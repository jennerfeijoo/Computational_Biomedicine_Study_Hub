# Auditoría académica, funcional y arquitectónica

Fecha de la línea base: 2026-07-19  
Rama: `feat/learning-engine-global-pages`  
Alcance: estado anterior a la evolución del motor transversal.

## Resumen ejecutivo

DM857 es un catálogo académico real y reutilizable: contiene 14 módulos completos en
español, inglés y danés, IDs estables, bancos objetivos independientes y validaciones de
alineación lingüística. La carga diferida de lectores y secciones evita construir de golpe
la interfaz de todos los módulos. Esta base debe conservarse.

El producto, sin embargo, todavía no implementa el ciclo de aprendizaje declarado de
extremo a extremo. Review, Assessments, Flashcards y Glossary son `PlaceholderPage`; la
práctica abierta sólo conserva estado en memoria; sólo las preguntas objetivas de opción
única y verdadero/falso tienen corrección interactiva específica; y no existe persistencia
de intentos, sesiones, dominio ni repetición espaciada. El cambio de idioma reconstruye las
páginas y pierde respuestas no persistidas.

La prioridad P0 es introducir una capa de progreso offline con IDs independientes del
idioma y un motor de renderizado por tipo. Sobre esas dos piezas pueden construirse las
páginas globales sin duplicar contenido ni reescribir el lector. No conviene producir aún
catálogos extensos para DM847, BMB830 o BMB831: primero debe estabilizarse el contrato que
los consumirá.

## Estado por asignatura

| Curso | Contenido académico | Interfaz | Evaluación | Estado real |
|---|---|---|---|---|
| DM857 | 14 bundles trilingües, 14 módulos, bancos objetivos de 20–30 preguntas y evaluaciones abiertas/mixtas | Navegación por módulo y lector de cinco pestañas con construcción diferida | Banco objetivo interactivo; `assessment_items` sólo se muestran como tarjetas estáticas en el lector | Contenido terminado; experiencia de aprendizaje parcial |
| DM847 | Registro trilingüe y esquema general de bioinformática | Página de descripción | Sin módulos ni bancos | Estructura |
| BMB830 | Registro trilingüe y esquema general de bioestadística en R I | Página de descripción | Sin módulos ni bancos | Estructura |
| BMB831 | Registro trilingüe y esquema general de bioestadística en R II | Página de descripción | Sin módulos ni bancos | Estructura |

## Cobertura de DM857 frente al programa oficial

La referencia comprobada es la descripción vigente de
[DM857 en ODIN, University of Southern Denmark](https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=DM857&lang=en).
Los resultados oficiales cubren modelado de problemas, diseño e implementación de
programas, uso de bibliotecas, pruebas, recursión, tipos abstractos de datos, árboles y
programación estructurada.

La cobertura conceptual es alta:

- modelado, estado y descomposición: módulos 1 y 4;
- secuencia, selección, repetición y subprogramas: módulos 1–4;
- listas, mapas y otras estructuras: módulos 5–8;
- recursión: módulo 9;
- árboles: módulo 10;
- tipos abstractos, contratos y objetos: módulos 11–12;
- bibliotecas y computación científica: módulo 13;
- testing, depuración y calidad: módulo 14.

La matriz detallada está en [course_coverage_matrix.md](course_coverage_matrix.md).
La carencia académica principal no es un tema aislado, sino una experiencia integradora
evaluada que conecte modelo, implementación, pruebas e interpretación. También faltan un
flujo específico para preparar el informe del proyecto y una simulación persistente de
presentación/defensa oral, formas de evaluación incluidas en la descripción oficial.

## Mapa arquitectónico actual

```text
content/
  models.py, localized_models.py       modelos académicos sin PySide6
  bundles.py                           módulo + banco objetivo + versión
  dm857/                               autoría y catálogo de 14 módulos
learning/
  activity_types.py                    taxonomía
  objective_assessment.py              muestreo y corrección objetiva por option_id
  guided_practice.py                   muestreo de ejercicios
tutoring/
  context.py                           recuperación léxica y construcción del prompt
integrations/
  ollama.py, ollama_chat.py            transporte HTTP local y validación de protocolo
courses/
  dm857.py                             navegación diferida del catálogo
  dm847.py, bmb830.py, bmb831.py       páginas estructurales
ui/
  main_window.py, routes.py            composición y navegación global
  pages/module_reader_page.py          lector y pestañas diferidas
  widgets/                             práctica y banco objetivo
tests/                                 185 pruebas en la línea base
```

La separación de contenido, dominio y transporte es una base válida. Las dependencias
problemáticas aparecen al componer la experiencia: `MainWindow` conoce todas las páginas,
el lector decide cómo representar cada actividad y los widgets mantienen estado de
aprendizaje efímero. No se detectaron ciclos de importación en la línea base, pero no existe
todavía un contrato de repositorio que impida que la futura persistencia termine dentro de
widgets.

## Inventario real de ActivityType y renderizado

“Soportado” exige modelo, interfaz, interacción, corrección o autoevaluación apropiada,
persistencia y tests. En la línea base ningún tipo cumple las cinco dimensiones.

| ActivityType | Interfaz actual | Interacción/corrección | Persistencia | Estado |
|---|---|---|---|---|
| `WORKED_EXAMPLE` | Tarjeta de lectura | Sólo lectura | No | Parcial |
| `FLASHCARD` | Sin página funcional | No | No | Ausente |
| `MULTIPLE_CHOICE` | `ObjectiveQuestionCard` en banco; editor genérico en práctica | Corrección por `option_id` sólo en banco objetivo | No | Parcial |
| `MULTIPLE_SELECT` | Editor/tarjeta genérica | Sin selección múltiple interactiva | No | Parcial |
| `TRUE_FALSE` | `ObjectiveQuestionCard` en banco | Corrección por `option_id` sólo en banco objetivo | No | Parcial |
| `FILL_IN_THE_BLANK` | `QPlainTextEdit` genérico | Respuesta libre y referencia | No | Parcial |
| `MATCHING` | Editor/tarjeta genérica | Sin interacción de emparejamiento | No | Parcial |
| `ORDERING` | Editor/tarjeta genérica | Sin reordenación interactiva | No | Parcial |
| `CODE_COMPLETION` | Editor genérico con código inicial | Autoevaluación binaria | No | Parcial |
| `CODE_TRACING` | Editor genérico | Autoevaluación binaria | No | Parcial |
| `DEBUGGING` | Editor genérico con código inicial | Autoevaluación binaria | No | Parcial |
| `SHORT_ANSWER` | Editor genérico | Autoevaluación binaria | No | Parcial |
| `ORAL_EXPLANATION` | Editor genérico | No hay ensayo oral ni escala parcial | No | Parcial |
| `DATA_INTERPRETATION` | Editor genérico | No hay visualización ni rúbrica operativa | No | Parcial |
| `PIPELINE_DESIGN` | Editor genérico | No hay constructor ni rúbrica operativa | No | Parcial |
| cloze con opciones | No existe tipo ni modelo | No | No | Ausente |

`GuidedPracticeCard` ofrece pistas, solución de referencia y estados `solved/review`, pero
no representa las semánticas de selección, relación u ordenación y carece del estado
`partial`. `ModuleReaderPage._assessment_card()` sólo imprime opciones y respuesta, por lo
que la presencia de `AssessmentItem` no equivale a una evaluación funcional.

## Persistencia disponible

`LanguageController` y la configuración de Ollama usan `QSettings`. No existe almacenamiento
para intentos, respuestas, sesiones, dominio, tarjetas ni fechas de repaso. Los resultados
de `GuidedPracticeWidget` y `ObjectiveAssessmentWidget` viven en diccionarios de los
widgets. Una nueva sesión los reemplaza; reconstruir páginas por un cambio de idioma
también los descarta.

Los modelos objetivos ya contienen la decisión correcta para persistir con seguridad:
`AssessmentOption.option_id` y `AssessmentItem.correct_option_ids` son independientes del
texto visible. El nuevo esquema debe conservar además `course_code`, `module_id`,
`item_id`/`exercise_id`, `content_version` y la locale sólo como metadato, nunca como clave
de corrección.

## Accesibilidad, navegación y rendimiento

### Terminado

- lectores de módulo y sus cinco secciones se construyen bajo demanda;
- `QStackedWidget` mantiene una única ruta visible;
- al reemplazar páginas se llama a `deleteLater`;
- los botones de idioma tienen nombre accesible;
- las áreas académicas largas usan scroll.

### Parcial o ausente

- no hay estrategia global de foco al cambiar de ruta, módulo o pestaña;
- faltan nombres/descripciones accesibles en controles de práctica y evaluación;
- no se define un orden de tabulación probado;
- matching y ordering no se pueden operar porque aún no son controles reales;
- no hay atajos documentados para navegación principal;
- el cambio de idioma preserva curso/módulo/pestaña, pero no sesión ni respuestas;
- las páginas globales se construyen al iniciar aunque sean placeholders; el catálogo
  académico de DM857 sí conserva carga diferida;
- no existen pruebas de textos extensos daneses, escalado de fuente, tamaños mínimos,
  contraste o navegación sólo con teclado.

## Ollama

La arquitectura separa correctamente recuperación (`TutorDocumentRetriever`), construcción
de prompt (`ModuleTutorPromptBuilder`) y transporte (`OllamaChatClient`). La recuperación
se limita a un `LearningModule`, incluye IDs de fuente y el prompt delimita el contenido
recuperado como material, no como instrucciones. El transporte tiene timeouts y errores
tipados. La comprobación desde Settings usa `QThread`.

Siguen faltando una interfaz de tutor de módulo, cancelación cooperativa de una generación,
streaming y un coordinador de tareas que garantice que ninguna llamada de generación
bloquee el hilo principal. `ModuleTutorPromptBuilder` fija español, por lo que no respeta la
locale activa. La recuperación está aislada por módulo, pero el futuro modo acumulativo
deberá filtrar explícitamente curso e idioma. El texto recuperado se delimita, aunque una
defensa adicional debe serializarlo como datos y mantener las instrucciones exclusivamente
en el mensaje de sistema.

## Cobertura de tests de la línea base

La línea base contiene 185 pruebas y pasa `pytest`, `ruff check`, `ruff format --check` y
`mypy --strict`. La suite verifica con rigor:

- catálogo de 14 bundles, unicidad y prefijos de IDs;
- materialización en las tres locales y alineación de opciones;
- corrección objetiva por `option_id`;
- carga diferida de lectores y pestañas;
- navegación y reconstrucción al cambiar idioma;
- recuperación/prompt y transporte de Ollama;
- cantidades y taxonomía mínima de los módulos.

Las cantidades exactas (`12` prácticas, `14` evaluaciones, `30` preguntas) aparecen en
muchas pruebas. Son útiles como guardia contra pérdida accidental, pero no demuestran la
relación entre objetivo y actividad ni el comportamiento de cada renderer. Faltan pruebas
de persistencia/reinicio, migración, repetición espaciada, páginas globales, respuestas
abiertas parciales, estados vacíos, teclado, progreso agregado, errores de base de datos y
sesiones conservadas al cambiar de idioma.

## Deuda técnica y riesgos de escalabilidad

| Prioridad | Evidencia y riesgo | Decisión incremental |
|---|---|---|
| P0 | Estado de aprendizaje en widgets (`GuidedPracticeWidget`, `ObjectiveAssessmentWidget`) | Crear entidades de dominio, protocolo de repositorio y SQLite versionado |
| P0 | `GuidedPracticeCard` representa tipos semánticamente distintos como texto libre | Introducir registro `ActivityType -> renderer`, reutilizable por práctica y Assessments |
| P0 | `MainWindow._register_pages()` registra cuatro placeholders | Sustituirlos por páginas que consuman catálogo y repositorio |
| P0 | El lector duplica la evaluación: banco interactivo y `assessment_items` estáticos | Mantener sólo el banco en el lector y reutilizar authored items globalmente |
| P1 | No existe cloze estructurado; texto visible sería una clave frágil | Modelar huecos y opciones con IDs trilingües y evaluación por ID |
| P1 | Cambio de idioma destruye respuestas activas | Persistir sesión/selecciones antes de reconstruir y restaurarlas por IDs |
| P1 | Archivos de autoría DM857 alcanzan aproximadamente 900–1100 líneas y repiten constructores | Conservarlos ahora; extraer gradualmente builders validados y, después, evaluar recursos estructurados |
| P1 | No hay relación formal objetivo–actividad en el modelo | Añadir metadatos de cobertura sin cambiar IDs ni contenido existente |
| P1 | No hay proyecto integrador, informe ni flujo oral persistente | Añadir modalidades de evaluación global sobre los contenidos existentes |
| P2 | `ModuleTutorPromptBuilder` fija español | Parametrizar locale y probar aislamiento curso/módulo/idioma |
| P2 | Accesibilidad probada sólo de forma puntual | Establecer contrato de foco, nombres accesibles y pruebas de teclado |

Los archivos Python declarativos ofrecen tipado inmediato y validación al importar, pero a
50 o más módulos aumentarán el coste de revisión, los conflictos y la repetición
trilingüe. No se recomienda una migración masiva ahora. El paso seguro es definir primero
un DTO/versionado y funciones `load -> validate -> materialize`; después un módulo piloto
puede serializarse a JSON o YAML y validarse con los mismos dataclasses. JSON es menos
amistoso para autoría larga; YAML mejora legibilidad pero añade una dependencia y exige
validar tipos implícitos; TOML no encaja bien con textos y listas profundamente anidados;
SQLite conviene para progreso, no como formato primario de contenido revisado en Git.

## Prioridades de ejecución

### P0

1. Persistencia SQLite segura y separada de PySide6.
2. Registro de renderers con corrección por IDs y autoevaluación honesta.
3. Eliminar la segunda sección visual del lector sin borrar `assessment_items`.
4. Activar Review, Assessments, Flashcards y Glossary sobre modelos.
5. Pruebas de reinicio, migración, idioma y compatibilidad de los 14 módulos.

### P1

1. Cloze de opciones con uno o varios huecos.
2. Progreso agregado, continuar y restauración de sesión.
3. Proyectos integradores, informe y defensa oral para DM857.
4. Contrato explícito de cobertura objetivo–actividad.
5. Accesibilidad y teclado.

### P2

1. Tutor local asíncrono, cancelable y sensible a idioma.
2. Piloto de autoría estructurada tras estabilizar el DTO.
3. Nuevos catálogos para DM847, BMB830 y BMB831.

## Secuencia futura propuesta para cursos en fase de estructura

Estas secuencias son arquitectura de información, no contenido académico declarado como
terminado:

- DM847: contexto biológico y secuencias; alineamiento; motivos; modelos probabilísticos y
  HMM; indexación/búsqueda; NGS y control de calidad; redes; integración ómica; proyecto.
- BMB830: flujo reproducible en R; estructura/calidad de datos; descriptiva y visualización;
  probabilidad; muestreo; inferencia; comparación de grupos; regresión; diagnóstico e
  interpretación; informe reproducible.
- BMB831: modelos avanzados; diseño y contrastes múltiples; control FDR; reducción
  dimensional; clustering; clasificación/validación; Bioconductor; pipelines ómicos;
  reproducibilidad; proyecto crítico.

Cada futuro módulo debe registrarse como bundle versionado y entrar en Review, Assessments,
Flashcards y Glossary sin que esas páginas conozcan el curso concreto.

## Resultado de la evolución incremental

La auditoría anterior describe la línea base. En esta rama se han abordado sus P0 sin
reescribir el catálogo:

- SQLite v1 y entidades de progreso independientes de PySide6;
- repetición espaciada determinista;
- registro exhaustivo de renderers y cloze multihueco por IDs;
- eliminación visual de la evaluación authored duplicada en el lector;
- Review, Assessments, Flashcards y Glossary funcionales;
- persistencia de práctica y banco objetivo al cambiar de idioma o reiniciar;
- progreso compacto de módulo y acción Continuar;
- tests específicos de migración, reinicio, locale, páginas, renderers y los 14 módulos.

La arquitectura resultante, el esquema y los límites pendientes están documentados en
[learning_engine_architecture.md](learning_engine_architecture.md).
