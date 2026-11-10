# libro-a-skill

Una skill de Claude Code que convierte un libro (EPUB, PDF con texto o PDF escaneado) en otra skill: una que aplica el método del autor a problemas reales y revisa textos, planes o diseños con sus criterios.

## Qué hace

1. **Extrae** el libro y lo parte por capítulos con scripts locales. No gasta tokens y el modelo nunca lee el libro entero.
2. **Ficha** cada capítulo con un agente por capítulo, en paralelo.
3. **Destila** las fichas en glosario, método, criterios y patrones, cada ítem con su fuente (capítulo y sección).
4. **Instala** la skill nueva en `~/.claude/skills/` y la **prueba** con tres casos: aplicar, revisar y un caso de control donde el método no corresponde.

## Instalación

Copiá la carpeta `libro-a-skill/` a `~/.claude/skills/`. Requisitos: Python 3.10 o superior y PyMuPDF (`pip install pymupdf`). Para PDF escaneados, Tesseract con los idiomas `spa` y `eng`.

Después, en Claude Code: «hacé una skill de este libro» y la ruta del archivo.

## Costo de referencia

Primer caso: Donella Meadows, *Thinking in Systems* (2008), un EPUB de 67.000 palabras. Nueve fichas, un destilado y tres pruebas: alrededor de 1,2 millones de tokens de Sonnet.

## Lo que aprendí

Está en `libro-a-skill/LECCIONES.md`. Lo más importante:

- Las fichas van con Sonnet. En la prueba, Haiku inventó un criterio que el capítulo no formula.
- Sin un «filtro previo» en la skill generada, Claude aplica el vocabulario del libro a cualquier cosa.
- Un tope total de palabras en el destilado hace que el agente recorte criterios que otros archivos siguen usando.

## Derechos

El texto del libro queda solo en tu carpeta de trabajo. La skill generada lleva paráfrasis con fuente y, como mucho, una cita breve por archivo. No subas ni compartas la carpeta de trabajo, ni publiques skills hechas con libros que no podés redistribuir.

## Idioma

Las instrucciones y las plantillas están en español rioplatense.

## Licencia

MIT. Ver `LICENSE`.
