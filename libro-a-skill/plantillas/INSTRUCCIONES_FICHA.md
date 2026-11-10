# Instrucciones para la ficha de un capítulo

Vas a leer **un capítulo** de un libro y escribir una ficha. Las fichas de todos los capítulos se van a destilar después en una skill para Claude con dos usos:

1. **Aplicar el método del libro** a un problema real (analizar, diagnosticar, diseñar).
2. **Revisar** un texto, plan o diseño con los criterios del libro.

Por eso la ficha no es un resumen: es un **inventario de herramientas**. Cada cosa que anotes tiene que servir para hacer o para evaluar algo. Si no sirve para ninguna de las dos, no va.

## Reglas

- **Escribí en español neutro**, con oraciones claras. La primera vez que aparezca un término técnico, poné el término original entre paréntesis: *stock (stock)*, *bucle de realimentación de balance (balancing feedback loop)*.
- **Parafraseá, no copies.** Como mucho, tres citas textuales por ficha, de menos de 15 palabras cada una, solo cuando la formulación exacta del autor importe. Van entre comillas y en el idioma original.
- **Solo lo que dice el capítulo.** No completes con lo que sabés del tema ni con otros autores. Si algo queda ambiguo, marcalo con `[ambiguo]`. Prueba para cada criterio, procedimiento o salida de una trampa: ¿podrías señalar el pasaje que lo sostiene? Si no, no va. Una consecuencia razonable que el autor no formula tampoco va.
- **Principios destacados:** si el capítulo resalta frases sueltas, recuadros, resúmenes o máximas (por ejemplo, una oración aislada entre párrafos que enuncia una regla), cada una tiene que aparecer en "Criterios de revisión".
- **Ubicación:** todos los ítems de todas las secciones, salvo "Idea central" y "Conexiones", terminan con el subtítulo de la sección del capítulo donde aparecen, entre corchetes: `[§ Resilience]`. Si el capítulo no tiene subtítulos, usá `[§ inicio]`, `[§ medio]` o `[§ final]`. En los PDF, agregá la página: `[§ Resilience, p. 76]`.
- **Extensión:** como mucho el tope que te indiquen en el pedido (contado con `wc -w`). Si te pasás, recortá ejemplos y procedimientos redundantes antes que criterios. Si el tope es **libre**, la sección es un resumen del propio autor (apéndice, conclusiones, decálogo): ahí la regla es ser completo, con todos los términos, principios, trampas y listas que traiga.
- **Varias secciones en una ficha:** si el pedido te da más de un archivo, hacé una sola ficha y usá el título de cada sección como ubicación: `[§ Note from the Editor]`.
- **Diagramas:** las figuras no se extrajeron; solo quedan sus epígrafes y algunas etiquetas sueltas. No inventes lo que mostrarían: describí a partir del texto.
- **Listas del autor:** si el capítulo trae una lista numerada u ordenada (niveles, pasos, tipos), va completa y en su orden, aunque haya que recortar otra cosa. Un capítulo con muchas anécdotas y pocas ideas lleva una ficha corta.
- **No incluyas** anécdotas que no ilustren un principio, datos biográficos, agradecimientos ni opiniones del autor que no se puedan usar como criterio.
- Una sección que no tenga contenido en este capítulo se escribe así: `(nada en este capítulo)`. No la rellenes.

## Formato de salida (Markdown, exactamente estas secciones)

```markdown
# Ficha: <título del capítulo>

- Fuente: <autor, año, título>
- Archivo: <nombre del .txt>
- Palabras del capítulo: <n>

## Idea central
2 a 4 oraciones: qué problema ataca el capítulo y qué propone.

## Conceptos
| Término (original) | Definición operativa | Cómo se reconoce en un caso real |
|---|---|---|
Solo los términos que el capítulo define o usa como herramienta. La definición es en palabras propias.

## Procedimientos y preguntas
Pasos, métodos o preguntas que el capítulo propone (o que se desprenden directamente de él) para analizar o intervenir.
Formulá cada uno como instrucción o pregunta que se le pueda hacer a un caso: "Identificá…", "¿Qué pasa si…?".

## Criterios de revisión
Principios del capítulo convertidos en algo verificable. Uno por línea, con este formato:
- **<Principio en una frase>.** Se cumple si: <señal observable>. Se viola si: <señal observable>. [§ …]

## Patrones y trampas
Estructuras típicas que el capítulo describe, con este formato (si las hay):
- **<Nombre>:** estructura → comportamiento que produce → cómo se sale o se aprovecha. [§ …]

## Ejemplos útiles
Los ejemplos del libro que mejor ilustran una herramienta, en una línea cada uno, con la herramienta que ilustran.

## Límites y advertencias
Lo que el autor dice que el método no hace, dónde falla o qué malinterpretaciones evitar.

## Conexiones
Remisiones explícitas a otros capítulos del libro, o conceptos que el capítulo usa sin definir (probablemente definidos en otro lado).
```

Guardá la ficha en la ruta que te indiquen, y respondé solo con una línea: la ruta y la cantidad de palabras de la ficha.
