"""Paso 2 de libro-a-skill: arma el plan de fichas a partir de uno o varios indice.tsv. Cero tokens.

Uso:
  python -I plan_fichas.py <carpeta_trabajo> <fuente1> [<fuente2> ...] [--apendice N-M] [--min 1500]

  <carpeta_trabajo>  donde se escribe plan.tsv y se crearán las fichas (fichas/)
  <fuenteK>          carpeta de una fuente ya extraída (tiene indice.tsv y capitulos/)
  --apendice F:N-M   secciones N a M de la fuente F (1 = primera fuente) son el resumen del autor:
                     van juntas, en una ficha sin tope. Se puede repetir.
  --min 1500         las secciones de contenido más cortas que esto se agrupan con las vecinas

Reglas:
  - Solo entran las secciones de tipo "contenido" (las "breve" y "omitir" quedan afuera).
  - Secciones cortas consecutivas se juntan hasta superar --min palabras.
  - Tope de cada ficha: 35 % de las palabras, entre 800 y 1800. Los apéndices del autor: sin tope (0).

Salida: <carpeta_trabajo>/plan.tsv con columnas
  ficha, fuente, secciones, archivos, palabras, tope, titulo
El SKILL.md indica cómo lanzar un agente por fila.
"""
import os, re, sys, csv, argparse


def leer_indice(carpeta):
    with open(os.path.join(carpeta, "indice.tsv"), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def tope(palabras):
    return max(800, min(1800, round(palabras * 0.35 / 50) * 50))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # -I ignora PYTHONIOENCODING
    ap = argparse.ArgumentParser()
    ap.add_argument("trabajo"); ap.add_argument("fuentes", nargs="+")
    ap.add_argument("--apendice", action="append", default=[])
    ap.add_argument("--min", type=int, default=1500)
    a = ap.parse_args()

    apendices = {}
    for x in a.apendice:
        m = re.fullmatch(r"(\d+):(\d+)-(\d+)", x)
        if not m:
            sys.exit(f"--apendice mal escrito: {x} (formato F:N-M)")
        apendices.setdefault(int(m.group(1)), []).append((int(m.group(2)), int(m.group(3))))

    varias = len(a.fuentes) > 1
    filas = []
    for k, fuente in enumerate(a.fuentes, 1):
        nombre = os.path.basename(os.path.normpath(fuente))
        pref = f"{nombre}__" if varias else ""
        secs = [s for s in leer_indice(fuente)]
        en_apendice = lambda n: any(lo <= n <= hi for lo, hi in apendices.get(k, []))

        # apéndices del autor: una ficha cada rango, sin tope
        for lo, hi in apendices.get(k, []):
            grupo = [s for s in secs if lo <= int(s["n"]) <= hi and s["tipo"] != "omitir"]
            if grupo:
                filas.append(dict(ficha=f"{pref}{int(grupo[0]['n']):02d}_apendice.md", fuente=fuente,
                                  secciones=",".join(s["n"] for s in grupo),
                                  archivos=",".join(s["archivo"] for s in grupo),
                                  palabras=sum(int(s["palabras"]) for s in grupo), tope=0,
                                  titulo="Apéndice: " + " / ".join(s["titulo"] for s in grupo)))

        grupo = []
        def cerrar():
            if not grupo:
                return
            pal = sum(int(s["palabras"]) for s in grupo)
            base = re.sub(r"\.txt$", "", grupo[-1]["archivo"])
            filas.append(dict(ficha=f"{pref}{base}.md", fuente=fuente,
                              secciones=",".join(s["n"] for s in grupo),
                              archivos=",".join(s["archivo"] for s in grupo),
                              palabras=pal, tope=tope(pal),
                              titulo=" / ".join(s["titulo"] for s in grupo)))
            grupo.clear()

        for s in secs:
            if s["tipo"] != "contenido" or en_apendice(int(s["n"])):
                continue
            grupo.append(s)
            if sum(int(x["palabras"]) for x in grupo) >= a.min:
                cerrar()
        cerrar()

    os.makedirs(os.path.join(a.trabajo, "fichas"), exist_ok=True)
    salida = os.path.join(a.trabajo, "plan.tsv")
    campos = ["ficha", "fuente", "secciones", "archivos", "palabras", "tope", "titulo"]
    with open(salida, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter="\t")
        w.writeheader(); w.writerows(filas)
    for r in filas:
        print(f"{r['ficha']:<55} {r['palabras']:>6} pal  tope {r['tope'] or 'libre':>5}  ({r['secciones']})")
    print(f"\n{len(filas)} fichas · {sum(int(r['palabras']) for r in filas)} palabras → {salida}")


if __name__ == "__main__":
    main()
