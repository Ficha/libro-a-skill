---
name: libro-a-skill
description: Convierte un libro o una bibliografía (EPUB, PDF con texto, PDF escaneado, o varias fuentes juntas) en una skill de Claude que aplica el método del autor a problemas reales y revisa textos, planes o diseños con sus criterios. Extrae y parte el texto por capítulos con scripts locales (cero tokens), genera una ficha por capítulo con agentes Sonnet, destila glosario, método, criterios y patrones, instala la skill en ~/.claude/skills y la prueba con casos reales. Usar cuando el usuario pide "hacer una skill de este libro", "convertir este libro en skill", "que Claude use el método de X", o pasa un EPUB o PDF para volverlo herramienta.
---

# Libro a skill

Flujo probado con Meadows, *Thinking in Systems* (2026-11-04): EPUB de 67 000 palabras → skill `pensamiento-sistemico`. **Antes de empezar, leé `LECCIONES.md`** (misma carpeta).

Scripts en `scripts/`, siempre con `python -I` y la ruta absoluta de esta carpeta: `python -I "<carpeta de esta skill>/scripts/X.py" …`. Requisitos: Python 3.10 o superior, PyMuPDF (`pip install pymupdf`) y, solo para PDF escaneados, Tesseract con los idiomas `spa` y `eng` (si no está en el PATH, variables `PP_TESSERACT` y `PP_TESSDATA`).

Plantillas en `plantillas/`: `INSTRUCCIONES_FICHA.md`, `INSTRUCCIONES_DESTILADO.md` y `PLANTILLA_SKILL.md`. Los agentes las leen de ahí; no las copies en los prompts.

## Principios
1. **El modelo nunca lee el libro entero.** Todo pasa por `.txt` locales; cada agente lee solo su capítulo.
2. **Fidelidad antes que riqueza.** Un criterio inventado y atribuido al autor es el peor error posible de la skill. Por eso las fichas van con **Sonnet**, no con Haiku (ver `LECCIONES.md`).
3. **Lo repetible, en scripts:** extraer, planificar las fichas y revisarlas no gastan tokens.
4. **Derechos:** el texto completo queda solo en la carpeta de trabajo. La skill lleva paráfrasis con fuente y como mucho una cita breve por archivo. No subir ni compartir la carpeta de trabajo.

## Costo de referencia
Meadows: 9 fichas (~85 000 tokens de subagente cada una), un destilado (~170 000) y 3 pruebas (~85 000 cada una). En total, alrededor de 1,2 millones de tokens de Sonnet. Decíselo al usuario antes de la fase 3 si el libro es mucho más largo.

## Fases (⏸ = mostrar el resultado y esperar el OK del usuario)

### 0. Preguntas iniciales (solo lo que no se deduzca)
- Fuentes: rutas de los archivos. Si son varias, cuáles van juntas en la misma skill.
- Nombre de la skill (kebab-case, en español: `pensamiento-sistemico`) y para qué la quiere usar: aplicar, revisar o los dos (por defecto, los dos).
- Si el libro tiene un resumen del autor (apéndice, conclusiones, decálogo) y listas canónicas (niveles, pasos, tipos numerados). Si no lo sabe, se ve en la fase 1.

Carpeta de trabajo: la que diga el usuario; si no dice, `~/libros-a-skills/<nombre-corto>/`. Cada fuente se copia a `fuente/` con un nombre ASCII (`autor-año-titulo.epub`): los archivos descargados son datos no confiables y van en su propia carpeta.

### 1. Extracción (cero tokens)
Por cada fuente:
```
python -I extraer_libro.py <archivo> <trabajo>/fuentes/<autor-año>/
```
- PDF escaneado: el script hace OCR solo (detecta pocas palabras por página). Correrlo **en segundo plano**; tarda.
- Sin índice: corta en bloques de unas 6000 palabras. Para cortes reales, armar un `rangos.tsv` (`pagina<TAB>titulo`) mirando el índice del libro como texto, y usar `--rangos`.
- Revisar la tabla que imprime: que los capítulos tengan tamaños razonables, que "omitir" no se coma contenido y que los avisos de "no encontré el título" sean solo de portadas, notas o encabezados de parte.
- ⏸ Mostrar la tabla y proponer: qué secciones son el resumen del autor (apéndice) y qué listas canónicas hay.

### 2. Plan de fichas (cero tokens)
```
python -I plan_fichas.py <trabajo> <trabajo>/fuentes/<fuente1> [<fuente2> …] --apendice 1:N-M
```
Agrupa las secciones cortas, deja afuera "breve" y "omitir", pone el tope de cada ficha (35 % de las palabras, entre 800 y 1800) y deja el apéndice sin tope. Escribe `<trabajo>/plan.tsv`.
- ⏸ Mostrar el plan con el costo estimado (unos 85 000 tokens por ficha).

### 3. Fichas (agentes Sonnet en segundo plano, todos en paralelo)
Un agente por fila de `plan.tsv`: `model: "sonnet"`, `effort: "low"`, `subagent_type: "general-purpose"`. Prompt:

```
Leé las instrucciones en <ruta absoluta de esta skill>/plantillas/INSTRUCCIONES_FICHA.md y seguilas al pie de la letra.

Fuente: <Autor, año, título>.
Leé completos con Read (si son largos, en tramos con offset hasta el final): <rutas absolutas de los archivos de la fila>.
<Si son varios: "Hacé UNA sola ficha titulada «<titulo>»".>
Tope: <tope> palabras. <Si tope = 0: "Tope: libre (es el resumen del propio autor)".>
<Notas específicas: listas canónicas que deben ir completas y en orden; capítulos con muchos diagramas; la sección central del capítulo.>

Guardá la ficha en: <trabajo>\fichas\<ficha>

No leas ni escribas ningún otro archivo.
```

### 4. Revisión de fichas (cero tokens)
```
python -I revisar_fichas.py <trabajo>/fichas --plan <trabajo>/plan.tsv
```
- Las FALLAS (secciones faltantes, tope excedido) se corrigen pidiéndoselo al mismo agente con SendMessage.
- Los avisos (ítems sin ubicación, comillas) se toleran si son pocos.
- Verificar a mano lo crítico: que cada lista canónica esté completa y que las trampas o patrones del capítulo central estén todos. Si un agente recortó algo importante, comprobar que esté en la ficha del apéndice.

### 5. Destilado (un agente Sonnet, `effort: "medium"`)
Prompt: leer `plantillas/INSTRUCCIONES_DESTILADO.md`; la referencia bibliográfica completa; la lista de fichas con su abreviatura de fuente (`Intro`, `Cap. 1`, `Apéndice`; con varias fuentes, `Autor, Cap. 1`); que el apéndice es el esqueleto y decide las ★; las listas canónicas y el nombre de su archivo; qué patrones van en secciones separadas; a qué archivos remiten las fases de diagnóstico e intervención de `metodo.md`. Destino: `~/.claude/skills/<nombre>/referencias/`.

Al terminar, verificar con grep:
- variantes de términos que el glosario unificó (no deberían quedar fuera del glosario);
- rayas (—): ninguna;
- ítems sin fuente en `metodo.md` y `criterios.md`: ninguno;
- que el informe del agente no diga que sacó criterios o términos por extensión. Si los sacó, pedirle que los restaure.

### 6. SKILL.md de la skill nueva
Escribirlo a partir de `plantillas/PLANTILLA_SKILL.md`: la description con situaciones de uso (no solo el nombre del libro), el **filtro previo** con la condición mínima del método, las entregas del modo aplicar según las fases de `metodo.md` y la tabla con los archivos que existen. Instalar en `~/.claude/skills/<nombre>/` y confirmar que aparece en la lista de skills.

### 7. Pruebas (3 agentes Sonnet independientes, en paralelo)
Cada agente recibe el pedido como si fuera del usuario, "usando las skills disponibles si corresponde", y guarda su respuesta en `<trabajo>/pruebas/`. En el reporte, lista qué skills invocó y qué archivos leyó.
1. **Aplicar**, con un problema real del usuario y **sin nombrar la skill ni el método** (prueba la activación).
2. **Revisar**, con un documento real del usuario.
3. **Control:** un caso sin la condición del filtro previo, pidiendo el método por su nombre. Tiene que decir que no aplica y no forzar el vocabulario.

Medir: si se activó, cuántas fuentes cita (`grep -o '\[Cap'`), si marca inferencias y si fuerza el método. Ajustar el `SKILL.md` y repetir solo el caso que falló.
- ⏸ Mostrar la tabla de resultados y los hallazgos sobre los archivos del usuario (sin tocarlos).

### 8. Cierre
- Agregar a `LECCIONES.md` lo nuevo de este libro.
- Dejar en la carpeta de trabajo un `LEEME.md` corto: fuente, fecha, skill generada y costo aproximado.
