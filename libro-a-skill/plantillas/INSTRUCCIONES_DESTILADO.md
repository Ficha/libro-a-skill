# Instrucciones para destilar las fichas en las referencias de una skill

Recibís las fichas de todos los capítulos de un libro (o de varias fuentes). Cada ficha tiene: Idea central, Conceptos, Procedimientos y preguntas, Criterios de revisión, Patrones y trampas, Ejemplos útiles, Límites y advertencias, Conexiones.

Tu trabajo es convertirlas en los **archivos de referencia** de una skill para Claude. La skill tiene dos modos:

1. **Aplicar el método** del libro a un problema real.
2. **Revisar** un texto, plan o diseño con los criterios del libro.

Quien use la skill va a leer estas referencias en medio de una tarea, así que tienen que ser **consultables**: ordenadas, sin repeticiones y con un término único para cada concepto.

## Reglas

- **Solo lo que está en las fichas.** No agregues contenido de tu conocimiento del tema ni de otros autores. Unir, ordenar y deduplicar sí; inventar no.
- **Un término por concepto.** Antes de escribir los demás archivos, armá el glosario y fijá una sola traducción para cada término (la más clara en español neutro, con el original entre paréntesis). Después usá **exactamente** esa traducción en todos los archivos, aunque las fichas usen variantes.
- **Fuente en cada ítem**, en este formato: `[Cap. 3 § Resilience]`, `[Intro § …]`, `[Apéndice § Traps]`. Si un ítem aparece en varias fichas, poné las fuentes juntas: `[Cap. 5 § Escalation; Apéndice § Traps]`. Para varias fuentes bibliográficas, anteponé el autor: `[Meadows, Cap. 3 § …]`.
- **Deduplicá en serio.** Si dos criterios dicen lo mismo con palabras distintas, quedate con la formulación más operativa y juntá las fuentes.
- **Marcá con ★ los principios que el propio autor destaca** (los que aparecen en su resumen o apéndice, o como frases resaltadas en las fichas).
- **Listas canónicas completas.** Si el autor propone una lista ordenada (por ejemplo, niveles, pasos o tipos numerados), va completa, en su orden y en su propio archivo.
- **Citas:** como mucho una cita textual por archivo, de menos de 15 palabras, en el idioma original.
- **Estilo:** español neutro, oraciones cortas, sin rayas (—); usá comas, dos puntos o paréntesis.
- **Extensión:** cada archivo hasta 3000 palabras. **No hay tope total**: las referencias se cargan por separado según el modo. Si un archivo se pasa, recortá ejemplos antes que criterios, y nunca saques del glosario un término que otro archivo usa.
- **Varias fuentes:** si las fichas vienen de más de una obra, el glosario unifica los términos entre autores. Cuando dos autores usan el mismo término con sentidos distintos, van en filas separadas (`Resiliencia (Meadows)`, `Resiliencia (Holling)`). Cuando se contradicen, el criterio o patrón lleva las dos posiciones con su fuente y una línea que marque el desacuerdo: no lo resuelvas por tu cuenta.

## Archivos que tenés que escribir

### `glosario.md`
Tabla: `| Término (original) | Definición operativa | Cómo se reconoce en un caso | Fuente |`. Ordenada alfabéticamente por el término en español.

### `metodo.md`
El procedimiento para **aplicar** el método, como una secuencia de fases que alguien pueda seguir frente a un caso nuevo. Cada fase tiene: propósito en una línea, preguntas o instrucciones (con fuente) y qué produce. El orden sigue la lógica del libro (normalmente: delimitar el problema y su comportamiento en el tiempo → estructura → dinámica → diagnóstico → intervención). Al final, una sección **Límites del método**, con los límites y advertencias de las fichas, deduplicados.

### `criterios.md`
La checklist para **revisar**, agrupada por tema (de 4 a 8 grupos con título). Formato de cada ítem:
`- [ ] **<Principio>.** Se cumple si: … Se viola si: … [fuente]` (con ★ delante del principio si corresponde).

### `patrones.md`
Los patrones y trampas que el libro describe. Para cada uno: nombre (original), estructura, comportamiento que produce, **señales para detectarlo en un caso**, salida o forma de aprovecharlo, un ejemplo del libro en una línea y la fuente.

### `<lista-canonica>.md` (uno por cada lista canónica del autor, si las hay)
La lista completa en el orden del autor. Para cada elemento: qué es, una pregunta para detectarlo en un caso, un ejemplo del libro y la fuente. Abrí con una línea que explique el criterio del orden.

### `fuentes.md`
Una tabla que relaciona cada abreviatura de fuente (`Cap. 3`, `Apéndice`…) con el título completo del capítulo, y la referencia bibliográfica completa del libro.

## Al terminar
Respondé solo con la lista de archivos escritos, las palabras de cada uno y cualquier conflicto que no hayas podido resolver (por ejemplo, dos fichas que se contradicen).
