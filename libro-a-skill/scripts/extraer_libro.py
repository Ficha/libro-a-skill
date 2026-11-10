"""Bloque 1 de libro-a-skill: pasa un libro (EPUB, PDF con texto o PDF escaneado) a capítulos en .txt. Cero tokens.

Uso:
  python -I extraer_libro.py <libro.epub|libro.pdf> <carpeta_salida> [opciones]

Opciones:
  --idioma spa+eng   idiomas de Tesseract para PDF escaneados (por defecto: spa+eng)
  --nivel N          nivel del índice que define los capítulos (por defecto: 1; usa 2 si el nivel 1 tiene menos de 3 entradas)
  --rangos f.tsv     cortes a mano para libros sin índice: líneas "pagina_inicio<TAB>titulo" (páginas desde 1)
  --forzar           sobrescribe una extracción anterior

Salida:
  <salida>/capitulos/NN_titulo.txt   un archivo por capítulo, con párrafos unidos (sin cortes de línea internos)
  <salida>/indice.tsv                n, tipo, palabras, paginas, titulo, archivo

Tipos en el índice: "contenido" (va a los agentes), "breve" (menos de 150 palabras, por ejemplo una portadilla de parte)
y "omitir" (portada, créditos, índice, notas, bibliografía, agradecimientos, sobre el autor).
En los PDF cada capítulo lleva marcas "=== pág. N ===" para poder citar; en los EPUB no, porque sus páginas no existen.
"""
import os, re, sys, bisect, shutil, argparse, tempfile, subprocess, unicodedata
from concurrent.futures import ThreadPoolExecutor
import pymupdf

TESSERACT = os.environ.get("PP_TESSERACT") or shutil.which("tesseract") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = (os.environ.get("PP_TESSDATA") or os.environ.get("TESSDATA_PREFIX")
            or os.path.join(os.path.dirname(TESSERACT), "tessdata"))
OCR_ENV = dict(os.environ, TESSDATA_PREFIX=TESSDATA, OMP_THREAD_LIMIT="1")  # sin el límite, los hilos se pisan

OMITIR = re.compile(
    r"^(antes del [ií]ndice|title page|copyright|dedication|contents|table of contents|cover|index|notes|bibliography|"
    r"acknowledg|editor.s acknowledg|about the author|also by|portada|cr[eé]ditos|dedicatoria|"
    r"[ií]ndice|sumario|notas|bibliograf|agradecimientos|sobre (el|la) autor)", re.I)


def limpiar_titulo(t):
    return re.sub(r"\s+", " ", t.replace("\ufffd", " ")).strip()


def slug(t, n=50):
    t = re.sub(r"[‐-―/]", " ", t)  # rayas y barras separan palabras; si no, se pegan al quitar lo no ASCII
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:n].rstrip("-") or "seccion"


def texto_pagina(page):
    """Une las líneas de cada bloque en un párrafo y deshace los cortes con guion."""
    parrafos = []
    for b in page.get_text("blocks"):
        if b[6] != 0:  # 1 = imagen
            continue
        t = re.sub(r"(\w)-\n(\w)", r"\1\2", b[4].strip())
        t = re.sub(r"\s*\n\s*", " ", t)
        if t:
            parrafos.append(t)
    return "\n\n".join(parrafos)


def ocr_pagina(doc_path, i, idioma, tmp):
    page = pymupdf.open(doc_path)[i]
    png = os.path.join(tmp, f"p{i}.png")
    page.get_pixmap(dpi=300, colorspace=pymupdf.csGRAY).save(png)
    tess = lambda img, *a: subprocess.run([TESSERACT, img, "-", *a], capture_output=True, env=OCR_ENV).stdout.decode("utf-8", "replace")
    # escaneos al revés o de costado: se detecta la orientación (OSD) y se endereza    m = re.search(r"Rotate: (\d+)", tess(png, "--psm", "0"))
    from PIL import Image
    im = Image.open(png)
    if m and m.group(1) != "0":
        im = im.rotate(-int(m.group(1)), expand=True); im.save(png)
    w, h = im.size
    imgs = [png]
    if w > h * 1.15:  # doble página escaneada: se parte en dos
        im.crop((0, 0, w // 2, h)).save(png[:-4] + "a.png"); im.crop((w // 2, 0, w, h)).save(png[:-4] + "b.png")
        imgs = [png[:-4] + "a.png", png[:-4] + "b.png"]
    t = "\n\n".join(tess(i, "-l", idioma, "--psm", "3") for i in imgs)
    t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)
    return "\n\n".join(re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", t) if p.strip())


def leer_paginas(path, idioma):
    doc = pymupdf.open(path)
    textos = [texto_pagina(p) for p in doc]
    es_pdf = path.lower().endswith(".pdf")
    palabras = sum(len(t.split()) for t in textos)
    if es_pdf and palabras / max(len(textos), 1) < 60:
        if not os.path.exists(TESSERACT):
            sys.exit(f"PDF escaneado y no encuentro Tesseract en {TESSERACT} (variable PP_TESSERACT).")
        print(f"PDF escaneado: OCR de {len(textos)} páginas ({idioma}). Tarda; conviene correrlo en segundo plano.", flush=True)
        tmp = tempfile.mkdtemp()
        with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
            textos = list(pool.map(lambda i: ocr_pagina(path, i, idioma, tmp), range(len(textos))))
        shutil.rmtree(tmp, ignore_errors=True)
        return doc, textos, es_pdf, "OCR"
    return doc, textos, es_pdf, "texto"


def entradas(doc, nivel, rangos):
    """Devuelve [(titulo, pagina_inicio_0)] ordenadas."""
    if rangos:
        out = []
        with open(rangos, encoding="utf-8") as f:
            for linea in f:
                if linea.strip() and not linea.startswith("#"):
                    p, t = linea.rstrip("\n").split("\t", 1)
                    out.append((limpiar_titulo(t), int(p) - 1))
        return sorted(out, key=lambda x: x[1])
    # Los PDF exportados de Word traen marcadores internos como índice (_GoBack, _Hlk123, B12): se descartan
    basura = re.compile(r"^(_|[A-Z]?\d+$|$)")
    toc = [(l, limpiar_titulo(t), p - 1) for l, t, p in doc.get_toc()
           if p >= 1 and not basura.match(limpiar_titulo(t))]
    if len(toc) < 2:
        return []
    if nivel == 1 and sum(1 for l, _, _ in toc if l == 1) < 3:
        nivel = 2
    return [(t, p) for l, t, p in toc if l <= nivel]


def cortes_por_titulo(completo, inicio_pag, ents, buscar=True):
    """Ubica cada entrada del índice en el texto: busca su título como comienzo de párrafo.
    La página del índice no alcanza: en los EPUB varias secciones de un mismo archivo HTML
    reciben la misma página o una equivocada. Los títulos de 3 palabras o más se buscan también
    antes de su página (desde el corte anterior); los cortos ("Notes", "Appendix") solo desde su página,
    para no confundirlos con texto corrido. Si no aparece, se corta al comienzo de su página."""
    paginas = sorted({p for _, p in ents})
    cortes, no_hallados, lo = [], [], 0
    for k, (t, p) in enumerate(ents):
        palabras = re.findall(r"\w+", t)
        siguiente = next((q for q in paginas if q > p), None)
        hi = inicio_pag[siguiente] if siguiente is not None else len(completo)
        # hacia atrás, como mucho hasta la página de la entrada anterior: así no se confunde con el índice del libro
        previa = inicio_pag[ents[k - 1][1]] if k else 0
        desde = max(lo, previa) if len(palabras) >= 3 else max(lo, inicio_pag[p])
        if not buscar:  # bloques artificiales (libro sin índice): se corta en la página
            cortes.append(max(lo, inicio_pag[p])); lo = cortes[-1] + 1
            continue
        m = None
        if palabras:
            # comienzo de párrafo, o primera línea de una página de PDF (después de la marca "=== pág. N ===")
            patron = r"(?:^|\n\n|(?P<pag>=== pág\. \d+ ===\n))\W*" + r"\W+".join(map(re.escape, palabras))
            todas = list(re.compile(patron, re.I).finditer(completo, desde, max(hi, desde)))
            # se prefiere la aparición en su propia página; antes de ella puede estar el índice del libro
            m = next((x for x in todas if x.start() >= inicio_pag[p] - 2), todas[0] if todas else None)
        if m:
            if m.group("pag"):
                c = m.start("pag")  # el corte incluye la marca de página
            else:
                c = m.start() + (2 if completo.startswith("\n\n", m.start()) else 0)
        else:
            c = max(lo, inicio_pag[p]); no_hallados.append(t)
        cortes.append(c); lo = c + 1
    return cortes, no_hallados


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # -I ignora PYTHONIOENCODING
    ap = argparse.ArgumentParser()
    ap.add_argument("libro"); ap.add_argument("salida")
    ap.add_argument("--idioma", default="spa+eng"); ap.add_argument("--nivel", type=int, default=1)
    ap.add_argument("--rangos"); ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()

    caps_dir = os.path.join(a.salida, "capitulos")
    if os.path.isdir(caps_dir) and os.listdir(caps_dir):
        if not a.forzar:
            sys.exit(f"Ya hay una extracción en {caps_dir}. Usá --forzar para rehacerla.")
        for f in os.listdir(caps_dir):  # se borran los archivos, no la carpeta (puede estar abierta en otro proceso)
            os.remove(os.path.join(caps_dir, f))
    os.makedirs(caps_dir, exist_ok=True)

    doc, textos, es_pdf, como = leer_paginas(a.libro, a.idioma)
    n = len(textos)
    ents = entradas(doc, a.nivel, a.rangos)
    aviso = ""
    if not ents:  # sin índice: bloques de ~6000 palabras, cortados en límites de página
        aviso = "Sin índice: corté en bloques de ~6000 palabras. Para cortes reales, usá --rangos."
        ents, acum = [("Bloque 1", 0)], 0
        for i, t in enumerate(textos):
            if acum > 6000:
                ents.append((f"Bloque {len(ents) + 1}", i)); acum = 0
            acum += len(t.split())
        if len(ents) > 1 and acum < 1500:  # un último bloque muy corto se suma al anterior
            ents.pop()

    # texto completo con el desplazamiento donde empieza cada página
    trozos, inicio_pag, pos = [], [], 0
    for i, t in enumerate(textos):
        s = (f"=== pág. {i + 1} ===\n{t}" if es_pdf else t) + "\n\n"
        inicio_pag.append(pos); trozos.append(s); pos += len(s)
    completo = "".join(trozos)

    cortes, sin_cortar = cortes_por_titulo(completo, inicio_pag, ents, buscar=not aviso)
    if cortes and cortes[0] > 0 and completo[:cortes[0]].strip():  # texto antes de la primera entrada
        ents = [("Antes del índice", 0)] + ents; cortes = [0] + cortes
    secciones = []
    for k, (t, _) in enumerate(ents):
        a0, a1 = cortes[k], (cortes[k + 1] if k + 1 < len(cortes) else len(completo))
        pag = lambda off: bisect.bisect_right(inicio_pag, off)  # página (desde 1) de un desplazamiento
        secciones.append((t, f"{pag(a0)}-{pag(max(a1 - 1, a0))}", completo[a0:a1].strip()))

    with open(os.path.join(a.salida, "indice.tsv"), "w", encoding="utf-8") as idx:
        idx.write("n\ttipo\tpalabras\tpaginas\ttitulo\tarchivo\n")
        for i, (t, rango, cuerpo) in enumerate(secciones, 1):
            pal = len(cuerpo.split())
            tipo = "omitir" if OMITIR.match(t) else ("breve" if pal < 150 else "contenido")
            nombre = f"{i:02d}_{slug(t)}.txt"
            with open(os.path.join(caps_dir, nombre), "w", encoding="utf-8") as f:
                f.write(f"# {t}\n\n{cuerpo}\n")
            idx.write(f"{i}\t{tipo}\t{pal}\t{rango}\t{t}\t{nombre}\n")
            print(f"{i:>3}  {tipo:<9} {pal:>6}  {t}")

    total = sum(len(c.split()) for _, _, c in secciones)
    util = sum(len(c.split()) for t, _, c in secciones if not OMITIR.match(t))
    print(f"\n{len(secciones)} secciones · {total} palabras ({util} sin preliminares ni finales) · extracción por {como}")
    if aviso:
        print(aviso)
    for s in sin_cortar:
        print(f"Aviso: no encontré el título «{s}» en el texto; corté al comienzo de su página.")


if __name__ == "__main__":
    main()
