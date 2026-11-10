# Lecciones de libro-a-skill

Problemas ya resueltos y errores a no repetir. Primer caso: Meadows, *Thinking in Systems* (2026-11-04).

## Extracción
- En los EPUB, PyMuPDF asigna mal la página de las secciones que comparten un archivo HTML (apéndices). Por eso `extraer_libro.py` corta buscando cada título como comienzo de párrafo, y no solo por la página del índice.
- El índice del propio libro (Contents) repite todos los títulos como párrafos: se prefiere la aparición en la propia página de la entrada.
- Los diagramas son imágenes y no se extraen; solo quedan los epígrafes. Avisarle al agente del capítulo correspondiente que no invente lo que mostrarían.
- No borrar la carpeta de salida con `rmtree`: si está abierta en otro proceso, Windows la bloquea. Se borran los archivos.
- Los PDF exportados de Word traen como "índice" sus marcadores internos (`_GoBack`, `_Hlk…`, `B12`). El script los descarta y, si queda menos de 2 entradas, corta en bloques.
- En los PDF, un título que abre página queda justo después de la marca `=== pág. N ===`, no después de una línea en blanco: el patrón de búsqueda lo contempla.
- Los escaneos pueden venir al revés o de costado: sin detección de orientación (OSD de Tesseract) el OCR devuelve basura. Se endereza y se parten las dobles páginas. Un PDF de 8 páginas tarda ~50 s.
- `python -I` ignora `PYTHONIOENCODING`: los scripts reconfiguran la salida a UTF-8 ellos mismos.
- Probado con: EPUB con índice (Meadows), PDF con índice basura (Tosi), PDF sin índice (Lauria, 47 págs.) y PDF escaneado al revés (Giammatteo y Albano, 8 págs.).

## Fichas
- **Modelo: Sonnet.** En la prueba, Haiku inventó un criterio que el capítulo no formula, y además se pasó de extensión y omitió ubicaciones. La diferencia de costo no compensa un criterio falso atribuido al autor.
- Un tope fijo de 1500 palabras obliga a recortar contenido real en capítulos densos. Para capítulos de más de 7000 palabras, permitir 1800; mejor aún, escalar el tope con el largo.
- Si el libro tiene un apéndice o resumen del autor, hacerle una ficha completa sin tope: funciona como red de seguridad de lo que se pierde en los capítulos y como esqueleto del destilado (★).
- Agrupar secciones chicas (notas preliminares + introducción; las partes del apéndice) en una sola ficha.
- Las listas canónicas del autor (por ejemplo, los 12 puntos de apalancamiento) hay que pedirlas explícitamente completas y en orden en el prompt del agente.
- Las fichas traducen distinto el mismo término. Se resuelve en el destilado con un glosario único, no en las fichas.

## Destilado
- **No poner tope total de palabras.** Las referencias se cargan por separado según el modo; un tope total hizo que el agente recortara criterios y términos del glosario que otros archivos seguían usando. Tope por archivo: 3000 palabras.
- Pedir "deduplicá" sin tope total alcanza para mantener los archivos consultables.

## Pruebas de la skill generada
- Tres casos con agentes Sonnet independientes, que reciben el pedido como si fuera del usuario: uno de **aplicar** (formulado sin nombrar la skill, para probar que se active sola), uno de **revisar** y uno de **control** sin dinámica. Medir: si se activó, cuántas fuentes cita, si marca inferencias y si fuerza el método.
- El caso de control es el que más enseña. Sin un "filtro previo" explícito en el SKILL.md, la skill aplica el vocabulario del libro a cualquier cosa. Con el filtro, lo declara y usa solo lo que encaja; si el usuario pide el método por nombre, igual tiende a aplicar algo. Toda skill generada lleva su filtro previo de alcance.
- Abrir con una "respuesta corta" de 3 a 5 líneas: las respuestas completas rondan las 1500 palabras.
