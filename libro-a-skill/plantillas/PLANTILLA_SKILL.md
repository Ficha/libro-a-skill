---
name: {{nombre-en-kebab}}
description: {{Qué hace, en una oración: "Analiza … y revisa … con {{el método o marco}} de {{Autor}} ({{Título}}, {{año}}), con {{3 a 5 conceptos centrales}}."}} Usar cuando el usuario pide {{frases literales que usaría: "analizar con …", "usar {{Autor}}", "revisar con criterios de …"}}, {{y las situaciones típicas en que el método sirve aunque no lo nombre}}.
---

<!--
Plantilla de libro-a-skill. Reemplazá todo lo que está entre {{ }} y borrá este comentario.
- La description decide cuándo se activa la skill: tiene que nombrar las situaciones, no solo el libro. Máximo ~1000 caracteres.
- "Filtro previo" es obligatorio: sin él, la skill aplica el vocabulario del libro a cualquier cosa (lección del caso Meadows).
- "Modo aplicar" se arma con las fases de referencias/metodo.md: un ítem de entrega por fase, en el mismo orden.
- La tabla de referencias lista solo los archivos que existen.
-->

# {{Título corto de la skill}} ({{Autor}})

Skill destilada de {{"un solo libro" o "N fuentes"}}: {{referencia completa}}. Todo el contenido está en `referencias/`, con la fuente de cada ítem (`[Cap. 3 § …]`). La tabla de abreviaturas está en `referencias/fuentes.md`.

## Reglas

1. **Vocabulario único.** Usá los términos de `referencias/glosario.md`, con el original entre paréntesis la primera vez. No alternes sinónimos.
2. **Fuente e inferencia, separadas.** Lo que viene de la fuente lleva su referencia entre corchetes. Lo que deducís vos para el caso concreto va marcado como *inferencia*. Nunca presentes una inferencia como si fuera de {{Autor}}.
3. **Sin otros autores** salvo que el usuario lo pida{{; si son varias fuentes: "fuera de las incluidas en fuentes.md"}}.
4. **Datos, no supuestos.** Los datos de un caso no se inventan. Si faltan, pedilos o declará el supuesto en una línea.
5. **Leé solo lo que el modo necesita** (ver la tabla de referencias).
6. **Proporción.** En los dos modos, abrí con una **respuesta corta** de 3 a 5 líneas y después el desarrollo.

## Filtro previo: ¿el método aplica?

Antes de leer cualquier referencia, preguntate: {{la condición mínima para que el método sirva; por ejemplo, en Meadows: "¿hay algo que se acumula y que cambia en el tiempo por decisiones que dependen de su propio estado?"}}

- **Sí:** seguí con el modo que corresponda.
- **No:** decilo en una o dos oraciones y respondé la pregunta **sin el marco**: no leas referencias ni cites a {{Autor}}. Forzar el vocabulario del libro sobre un caso que no lo tiene es un error, aunque el usuario haya nombrado el método.
- **Solo una parte del caso cumple la condición:** aplicá el método solo a esa parte y decí cuál es.

## Elegir el modo

| El usuario… | Modo |
|---|---|
| trae un problema, una situación o una pregunta abierta | **Aplicar** |
| trae un texto, plan o diseño ya hecho para evaluar | **Revisar** |
| pide revisar y además proponer mejoras | **Revisar**, y después **Aplicar** solo sobre los puntos débiles |

## Modo aplicar

Leé `referencias/metodo.md` y seguí sus fases. {{Remisiones: "En el diagnóstico, buscá coincidencias en referencias/patrones.md; en la intervención, …"}}

Entregá, en este orden:

1. **{{Fase 1}}:** {{qué se entrega}}.
2. **{{Fase 2}}:** {{qué se entrega}}.
3. {{…}}
N. **Límites:** qué no se sabe, qué supuestos pesan y qué conviene observar para corregir el análisis.

{{Opcional: un diagrama en Mermaid si el método trabaja con estructuras o relaciones.}}

## Modo revisar

Leé `referencias/criterios.md`. {{Si corresponde: "Si lo revisado propone una intervención, leé también referencias/patrones.md"}}.

1. Recorré los grupos de criterios y quedate con los que aplican. No reportes los que no aplican.
2. Para cada criterio que aplica: **cumple / no cumple / sin datos**, la evidencia (cita breve o ubicación en el material revisado) y, si no cumple, una sugerencia concreta.
3. Ordená el informe: primero los incumplimientos de principios con ★, después el resto de los incumplimientos, al final lo que cumple, en una línea cada uno.
4. Cerrá con **los 3 cambios que más mejorarían el material**, cada uno con el criterio que lo justifica.

| Criterio | Veredicto | Evidencia | Sugerencia |
|---|---|---|---|

## Referencias

| Archivo | Qué tiene | Cuándo leerlo |
|---|---|---|
| `referencias/glosario.md` | Términos con definición operativa y cómo reconocerlos | Cuando dudes de un término o tengas que explicarlo |
| `referencias/metodo.md` | Fases para aplicar el método y sus límites | Modo aplicar, siempre |
| `referencias/criterios.md` | Checklist de revisión, con ★ en los principios del autor | Modo revisar, siempre |
| `referencias/patrones.md` | Patrones y trampas, con señales y salidas | {{cuándo}} |
| `referencias/{{lista-canonica}}.md` | {{qué}} | {{cuándo}} |
| `referencias/fuentes.md` | Abreviaturas de fuente y referencia completa | Para citar |
