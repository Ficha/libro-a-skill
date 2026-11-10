"""Revisa las fichas de una carpeta sin gastar tokens: secciones, extensión, ubicaciones y citas.

Uso: python -I revisar_fichas.py <carpeta_fichas> [--plan plan.tsv] [--max 1500]
Con --plan, el tope de cada ficha sale de plan.tsv (0 = sin límite); --max queda para fichas fuera del plan.
Ignora subcarpetas (por ejemplo, _prueba/). Sale con código 1 si alguna ficha tiene fallas.
Las fichas de resumen del autor (apéndices) se marcan con "Sin límite" en el nombre o se pasan en --sin-limite.
"""
import os, re, sys, argparse

SECCIONES = ["Idea central", "Conceptos", "Procedimientos y preguntas", "Criterios de revisión",
             "Patrones y trampas", "Ejemplos útiles", "Límites y advertencias", "Conexiones"]
CON_UBICACION = {"Procedimientos y preguntas", "Criterios de revisión", "Patrones y trampas",
                 "Ejemplos útiles", "Límites y advertencias"}


def revisar(path, maximo):
    txt = open(path, encoding="utf-8").read()
    fallas, avisos = [], []
    palabras = len(txt.split())
    if palabras > maximo:
        fallas.append(f"{palabras} palabras (máximo {maximo})")
    partes = re.split(r"^## ", txt, flags=re.M)
    secciones = {p.split("\n", 1)[0].strip(): p.split("\n", 1)[1] if "\n" in p else "" for p in partes[1:]}
    for s in SECCIONES:
        if s not in secciones:
            fallas.append(f"falta la sección «{s}»")
    sin_ubic = 0
    for s in CON_UBICACION & secciones.keys():
        for linea in secciones[s].splitlines():
            if re.match(r"\s*(- |\d+\. )", linea) and "nada en este capítulo" not in linea and "[§" not in linea:
                sin_ubic += 1
    if sin_ubic:
        avisos.append(f"{sin_ubic} ítems sin [§ …]")
    if "—" in txt:
        avisos.append("tiene rayas (—)")
    citas = len(re.findall(r"[\"“«][^\"”»\n]{3,}[\"”»]", txt))
    if citas > 3:
        avisos.append(f"{citas} fragmentos entre comillas (máximo 3 citas)")
    crit = len(re.findall(r"^\s*- \*\*", secciones.get("Criterios de revisión", ""), flags=re.M))
    return palabras, crit, fallas, avisos


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # -I ignora PYTHONIOENCODING
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta"); ap.add_argument("--max", type=int, default=1500)
    ap.add_argument("--sin-limite", nargs="*", default=[], help="nombres de fichas sin límite de palabras")
    ap.add_argument("--plan", help="plan.tsv de plan_fichas.py: toma el tope de cada ficha (0 = sin límite)")
    a = ap.parse_args()
    topes = {}
    if a.plan:
        import csv
        with open(a.plan, encoding="utf-8") as f:
            topes = {r["ficha"]: int(r["tope"]) for r in csv.DictReader(f, delimiter="\t")}
    hay_fallas = False
    print(f"{'ficha':<45} {'palabras':>8} {'criterios':>9}  estado")
    for f in sorted(os.listdir(a.carpeta)):
        p = os.path.join(a.carpeta, f)
        if not f.endswith(".md") or not os.path.isfile(p):
            continue
        maximo = topes.get(f, a.max) or 10**9
        if f in a.sin_limite:
            maximo = 10**9
        palabras, crit, fallas, avisos = revisar(p, maximo)
        hay_fallas |= bool(fallas)
        estado = "; ".join(["FALLA: " + x for x in fallas] + avisos) or "ok"
        print(f"{f:<45} {palabras:>8} {crit:>9}  {estado}")
    sys.exit(1 if hay_fallas else 0)


if __name__ == "__main__":
    main()
