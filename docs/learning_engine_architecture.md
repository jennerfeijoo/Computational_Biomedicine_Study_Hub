# Arquitectura del motor transversal de aprendizaje

Estado: implementación incremental de la rama
`feat/learning-engine-global-pages`.

## Decisiones

1. El contenido académico sigue siendo inmutable, trilingüe y versionado mediante
   `LocalizedModuleBundle`. No se han cambiado IDs ni eliminado elementos de DM857.
2. El progreso es un dominio separado de PySide6 y se persiste localmente con SQLite.
3. Los widgets consumen el protocolo `ProgressRepository`; no contienen SQL.
4. `ActivityRendererRegistry` resuelve `ActivityType -> renderer`. Las páginas no
   seleccionan widgets mediante texto visible ni mediante condicionales por asignatura.
5. La corrección objetiva usa `option_id`. Las respuestas abiertas conservan una respuesta
   de referencia y una rúbrica, y sólo admiten autoevaluación `solved`, `partial` o
   `review`.
6. Las páginas globales consumen `AcademicCatalog`, no inspeccionan widgets ya construidos.
7. No se ejecuta código Python o R del estudiante en el proceso de la interfaz.

## Límites de las capas

```text
content/
  modelos, texto trilingüe, bundles, IDs y versiones
learning/
  progreso, sesiones, catálogo de lectura, evaluación, cloze y repetición
persistence/
  rutas de datos y adaptación SQLite versionada
ui/activities/
  registro de renderers y widgets interactivos
ui/pages/
  coordinación de Review, Assessments, Flashcards y Glossary
courses/
  composición del lector y progreso de curso
```

Las dependencias se dirigen hacia el dominio. `persistence.sqlite_progress` implementa el
protocolo definido en `learning.progress_repository`; las páginas reciben ese protocolo
por constructor.

## Esquema SQLite v1

La versión se guarda en `PRAGMA user_version`. La inicialización es idempotente, transaccional
y rechaza una base creada por una versión futura de la aplicación.

### `attempts`

Registro inmutable de cada respuesta o autoevaluación:

- `attempt_id` (PK);
- `course_code`, `module_id`, `item_id`, `item_kind`;
- `activity_type`, `outcome`;
- `locale`, `content_version`;
- `created_at`;
- `response_text`;
- `selected_option_ids` como JSON de IDs;
- `is_correct`, `score`;
- `session_id`.

El texto visible puede conservarse como evidencia del estudiante, pero no participa en la
clave ni en la corrección.

### `practice_progress`

Último estado por `(course_code, module_id, exercise_id)`: dominio, intentos, resultado,
respuesta y fecha.

### `assessment_sessions`

Composición reproducible de una sesión:

- `session_id` (PK);
- ámbito: rápida, completa, curso, mixta, banco objetivo o práctica;
- curso y módulo;
- IDs de elementos;
- semilla;
- locale inicial;
- fecha de inicio/cierre;
- IDs respondidos y aciertos.

La semilla y los IDs permiten materializar la misma sesión con textos de otra locale.

### `flashcard_progress`

Estado SM-2 simplificado por `(course_code, module_id, card_id)`: repeticiones, intervalo,
facilidad, siguiente fecha, último repaso y dominio.

### `review_schedule`

Plan genérico por `(course_code, module_id, item_id, item_kind)`. Puede referirse a una
práctica, evaluación, tarjeta o concepto.

## Repetición espaciada

`learning.spaced_repetition.reschedule` es una función determinista y no importa PySide6.

- Again reinicia repeticiones, reduce facilidad y programa un día.
- Hard aumenta lentamente el intervalo y reduce facilidad.
- Good usa 1 día, 6 días y después multiplica por facilidad.
- Easy usa 4 días, 10 días y después un multiplicador ampliado.
- La facilidad queda limitada a `[1.3, 3.0]`.
- Las respuestas incorrectas y los estados `review/partial` entran de inmediato en Review;
  una calificación posterior calcula su nueva fecha.

## Renderers realmente registrados

| Tipo | Widget | Corrección |
|---|---|---|
| `multiple_choice` | radio buttons | conjunto de `option_id` |
| `multiple_select` | checkboxes | conjunto exacto de `option_id` |
| `true_false` | radio buttons | `option_id` |
| `fill_in_the_blank` | editor de texto | respuesta authored normalizada |
| `cloze_choice` | selector por hueco | mapa `gap_id -> option_id` |
| `matching` | selector por elemento | mapa de IDs izquierda/derecha |
| `ordering` | lista reordenable y botones de teclado | secuencia de `option_id` |
| `code_completion` | respuesta abierta | referencia, rúbrica y autoevaluación |
| `code_tracing` | respuesta abierta | referencia, rúbrica y autoevaluación |
| `debugging` | respuesta abierta | referencia, rúbrica y autoevaluación |
| `short_answer` | respuesta abierta | referencia, rúbrica y autoevaluación |
| `oral_explanation` | respuesta abierta | referencia, rúbrica y autoevaluación |
| `data_interpretation` | respuesta abierta | referencia, rúbrica y autoevaluación |
| `pipeline_design` | respuesta abierta | referencia, rúbrica y autoevaluación |

`worked_example` y `flashcard` también tienen entrada explícita en el registro para que la
taxonomía completa tenga un destino, aunque sus experiencias principales están en el lector
y en Flashcards.

Matching aprovecha las parejas authored actuales, delimitadas con flecha, pero evalúa la
selección mediante sus IDs. Antes de crear contenido nuevo conviene evolucionar el modelo
hacia lados izquierdo/derecho explícitos para no depender del delimitador al materializar.

## Cloze con opciones

`ClozeGap` contiene:

- `gap_id`;
- dos o más `AssessmentOption`;
- `correct_option_id`.

`LocalizedClozeGap` obliga a disponer de texto no vacío y opciones no duplicadas en los
tres idiomas. Cada prompt contiene un marcador `{gap_id}` por hueco. Serialización,
materialización y evaluación pasan siempre por los constructores validados.

## Flujos principales

### Lector de módulo

1. Se construye sólo el lector del módulo seleccionado.
2. Cada pestaña sigue construyéndose al abrirla por primera vez.
3. Practice crea o restaura una sesión por semilla e IDs.
4. Al revelar la solución, el estudiante elige resuelto, parcial o revisar.
5. Se guardan intento, respuesta, progreso y fecha de repaso.
6. Assessment muestra únicamente el banco objetivo aleatorio.
7. Una selección se corrige por ID y se guarda en la misma base.
8. Al cambiar de idioma, `MainWindow` conserva curso, módulo y pestaña; el nuevo widget
   restaura sesión, respuesta y selección con los textos de la nueva locale.

### Assessments

1. Se eligen curso, módulo, modalidad y `ActivityType`.
2. Rápida toma hasta 6 authored items; completa usa todos los del módulo; acumulativa y
   mixta toman hasta 20 elementos de su ámbito.
3. Cada `module.assessment_items` se presenta con el registro de renderers.
4. Cada resultado se guarda y una respuesta que necesita trabajo entra en Review.
5. Una sesión abierta se restaura tras reconstruir la página.

### Review

1. La cola consulta elementos vencidos con filtros de curso, módulo y tipo.
2. Puede mezclar cursos y añadir conceptos nuevos de dominio inicial bajo.
3. Muestra historial reciente y dominio estimado a partir de intentos persistidos.
4. Again/Hard/Good/Easy actualizan el algoritmo y retiran de la cola los elementos cuya
   siguiente fecha ya no está vencida.

### Flashcards

1. `AcademicCatalog` sintetiza tarjetas originales desde conceptos, puntos esenciales y
   errores frecuentes.
2. Los filtros no construyen lectores de módulo.
3. Se muestra anverso, se revela reverso y se califica.
4. La siguiente fecha, estadísticas y dominio sobreviven al reinicio.

### Glossary

1. Se agregan conceptos directamente desde modelos.
2. La búsqueda instantánea incluye término, definición, etiquetas, relacionados y
   sinónimos derivados.
3. El detalle muestra curso y módulo.
4. “Abrir módulo de origen” navega mediante `course_code/module_id`.

## Diseño pendiente para ejecución segura de Python y R

La implementación actual no ejecuta código arbitrario. Introducir `exec`, `eval`, un
intérprete embebido o `subprocess(..., shell=True)` dentro del proceso de PySide6 sería una
regresión de seguridad y estabilidad.

El futuro runner debe ser un adaptador independiente con este contrato:

```text
ExecutionRequest
  language: python | r
  source
  stdin
  timeout
  memory_limit
  output_limit
  allowed_files

ExecutionResult
  exit_code
  stdout
  stderr
  timed_out
  truncated
```

Requisitos mínimos:

1. crear un directorio temporal nuevo por intento;
2. escribir sólo archivos declarados;
3. lanzar `python -I` o `Rscript --vanilla` como lista de argumentos, nunca con shell;
4. fijar timeout y terminar el árbol de procesos;
5. limitar stdout/stderr y tamaño de archivos;
6. aplicar límites de CPU, memoria y procesos mediante el mecanismo del sistema operativo;
7. eliminar variables de entorno y credenciales no necesarias;
8. desactivar red mediante sandbox del sistema/contenedor, no mediante una promesa en el
   prompt;
9. permitir únicamente datasets copiados al directorio temporal como solo lectura;
10. ejecutar fuera del hilo principal y admitir cancelación;
11. distinguir fallo del runner, fallo del programa y resultado académico;
12. probar procesos infinitos, salida ilimitada, creación de hijos, rutas externas y
    señales de cancelación.

Sin aislamiento de red y procesos verificable en Windows, macOS y Linux, el runner debe
permanecer desactivado.

## Validación manual

1. Instalar el proyecto con dependencias de desarrollo.
2. Ejecutar `cb-study-hub`.
3. Abrir DM857, seleccionar un módulo y responder Practice.
4. Cambiar ES → EN → DK y comprobar módulo, pestaña, sesión y respuesta.
5. Cerrar y volver a abrir; comprobar el mismo progreso.
6. En Assessment del módulo, verificar que sólo aparece el banco objetivo.
7. En Assessments, iniciar una evaluación completa y comprobar actividades interactivas.
8. Fallar una respuesta, abrir Review y confirmar que aparece en la cola.
9. Calificar una tarjeta, reiniciar y comprobar estadísticas/fecha.
10. Buscar un término en Glossary y abrir el módulo de origen.

Para un entorno sin display:

```powershell
$env:QT_QPA_PLATFORM = "offscreen"
pytest
ruff check .
ruff format --check .
mypy
```

## Trabajo deliberadamente pendiente

- runner aislado de Python/R;
- interfaz de tutor Ollama por módulo, asíncrona y cancelable;
- streaming de tutor;
- audio para ensayo oral;
- proyectos integradores, preparación de informe y defensa de DM857;
- matching con lados estructurados en el modelo, sin delimitador textual;
- relación formal objetivo–actividad para informes automáticos de cobertura;
- catálogos académicos de DM847, BMB830 y BMB831;
- piloto de autoría externa JSON/YAML después de estabilizar el DTO.
