# Informe de integración del primer semestre

Fecha: 19 de julio de 2026

Rama: `feat/semester-1-learning-engine`

Base: `content/semester-1-complete-curriculum`

## Resultado ejecutivo

La aplicación dispone ahora de un motor offline-first común para cargar, localizar,
buscar y convertir en actividades el contenido YAML de las cuatro asignaturas. Los 54
módulos reales pueden materializarse mediante el lector reutilizable; las páginas
globales de Repaso, Evaluaciones, Tarjetas y Glosario son funcionales; Study Lab utiliza
el cliente Ollama existente fuera del hilo de Qt y sólo construye peticiones a partir de
evidencia recuperada; el progreso se almacena en SQLite mediante IDs estables.

La integración técnica no resuelve dos déficits editoriales demostrados por la
auditoría:

- existen **1.338 tarjetas**, no 1.344;
- DM857 contiene **420 tarjetas**, no 426;
- no existe una evaluación acumulativa canónica de DM857.

No se inventaron las seis tarjetas ni una evaluación para forzar los criterios. La
interfaz informa de la ausencia de la acumulativa de DM857 y el validador mantiene ambos
déficits como bloqueantes editoriales. Por ello, el criterio literal «1.344 tarjetas» y
la acumulativa de las cuatro asignaturas no pueden declararse completados.

## Arquitectura implementada

```text
academic_content/semester_1/
    fuente académica YAML canónica

academic/
    modelos inmutables, carga segura, validación, catálogo fuente,
    localización, fragmentación y recuperación BM25
academic/tutor/
    políticas, modos, prompts versionados, contexto y feedback tipado

learning/
    adaptación del catálogo a contratos existentes, progreso,
    repetición espaciada, recomendaciones y protocolos de repositorio

persistence/
    SQLite versionado y transaccional; ninguna página ejecuta SQL

ui/activities/
    renderers deterministas, incluidas actividades cloze y respuesta abierta
ui/pages/
    CourseStudy, Review, Assessments, Flashcards, Glossary y Study Lab

integrations/
    configuración, transporte y chat Ollama existentes
```

La dirección principal de dependencias es contenido → dominio académico/aprendizaje →
adaptadores → UI. Los modelos de `academic/` y `learning/progress.py` no importan
PySide6. Los widgets reciben `ProgressRepository`; el adaptador SQLite implementa ese
protocolo.

El YAML se incluye también dentro de la rueda mediante
`tool.hatch.build.targets.wheel.force-include`, y `default_content_root()` contempla
tanto el árbol de desarrollo como el recurso instalado.

## Contenido importado y conteos verificados

Se cargan 119 YAML no vacíos y válidos con `yaml.safe_load`.

| Asignatura | Módulos | Tarjetas | Glosario | Preguntas objetivas | Preguntas abiertas | Acumulativa |
|---|---:|---:|---:|---:|---:|---|
| BMB830 | 10 | 246 | 102 | 102 | 32 | Sí |
| BMB831 | 12 | 300 | 122 | 122 | 38 | Sí |
| DM847 | 15 | 372 | 162 | 152 | 47 | Sí |
| DM857 | 17 | 420 | 164 | 168 | 53 | No |
| **Total** | **54** | **1.338** | **550** | **544** | **170** | **3/4** |

Las 1.338 tarjetas tienen ID único, `front`/`back` completos y versiones ES/EN/DA. La
identidad cualificada de las demás entidades elimina las colisiones de 46 IDs fuente
históricamente locales sin cambiar esos IDs.

El índice inglés contiene actualmente 6.020 fragmentos independientes:

- 3.841 visibles;
- 2.179 de soporte oculto;
- conceptos, puntos clave, prompts y explicaciones de ejemplos, práctica, preguntas
  objetivas y abiertas, tarjetas y glosario se indexan por separado;
- cada hoja textual del soporte oculto se indexa como fragmento independiente.

Los números del índice pueden variar cuando se complete o corrija el corpus, por lo que
no son un contrato editorial.

## Correcciones estructurales del contenido

La auditoría y las correcciones completas están en `docs/content_audit_report.md`. En
resumen:

1. Se normalizaron de forma idempotente escalares YAML en 116 archivos.
2. Se repararon cuatro errores sintácticos puntuales.
3. Se corrigieron 11 referencias inequívocas de DM857 M01 al concepto existente.
4. Se ajustaron campos declarativos de cobertura a los objetos realmente almacenados:
   DM857 420, semestre 1.338.
5. Se añadió `scripts/normalize_semester_1_yaml.py` para reproducir la normalización.
6. El loader reconoce `template` como prompt de los tres cloze de DM857 que ya usaban
   esa variante estructural.

No se cambiaron explicaciones científicas, fórmulas, respuestas correctas, rúbricas ni
traducciones semánticas.

## Páginas y flujos implementados

### Cursos y módulos

`CourseStudyPage` permite reutilizar un único lector perezoso para cualquier curso YAML.
Expone resumen, resultados de aprendizaje, módulos, progreso, tarjetas vencidas, última
actividad y acceso a la acumulativa. Una prueba abre los 54 IDs y comprueba que cada
lector corresponde al módulo solicitado.

DM847, BMB830 y BMB831 usan esta página directamente desde `MainWindow`. DM857 conserva
por compatibilidad su composición especializada para los 14 módulos Python anteriores y
añade M15–M17 desde YAML. El catálogo global y las páginas transversales sí usan los 17
módulos YAML de DM857. Unificar también la composición visible de M01–M14 de DM857 queda
como migración incremental, no como reescritura.

`StudyLocation` conserva ruta, curso, módulo, pestaña, actividad, tarjeta, filtros,
borradores y posición lógica mediante datos serializables. El cambio de idioma reconstruye
las páginas conservando estado de curso/módulo/pestaña y la tarjeta/filtros actuales. Las
sesiones y borradores se restauran además desde SQLite mediante IDs.

### Tarjetas

`FlashcardsPage` estudia las 1.338 tarjetas authored, no tarjetas sintetizadas:

- tarjeta grande con scroll, anverso/reverso y pulsación sobre el cuerpo;
- Space/Enter para voltear; flechas para anterior/siguiente; 1–4 para valorar;
- Anterior, Siguiente, Voltear, Favorita, Reiniciar y Volver al módulo;
- filtros por curso, módulo, tipo, vencidas, nuevas, difíciles, favoritas y sesión mixta;
- botones Again/Hard/Good/Easy sólo tras revelar el reverso;
- transición de opacidad breve;
- progreso, dominio, historial de rating y próxima revisión persistentes.

### Repaso

`ReviewPage` mantiene una cola vencida calificable y seis bloques deterministas:

- Para hoy;
- Necesita refuerzo;
- Preguntas falladas;
- Tarjetas pendientes;
- Continuar donde lo dejaste;
- Progreso por asignatura.

`learning/recommendations.py` selecciona y justifica elementos usando intentos, errores,
fechas de vencimiento, tarjetas y progreso local. Ollama no decide la cola ni el
porcentaje.

### Evaluaciones

`AssessmentsPage` separa explícitamente:

1. evaluaciones objetivas;
2. preguntas abiertas;
3. evaluaciones acumulativas.

Mantiene ámbitos rápido, módulo completo, curso y semestre mixto, filtro por tipo,
composición aleatoria con semilla persistida y corrección por IDs. La pestaña Assessment
del módulo conserva el quiz objetivo y ya no duplica las tarjetas estáticas de preguntas
abiertas.

Las respuestas abiertas admiten texto extenso, confianza baja/media/alta, borrador,
versiones, referencia/rúbrica bajo acción explícita, autoevaluación y envío a Study Lab
para feedback local. Las acumulativas muestran el documento learner-visible y eliminan
recursivamente ramas de solución, respuesta canónica, guía de corrección y soporte
oculto antes de crear el widget. DM857 muestra una ausencia explícita.

### Glosario

`GlossaryPage` agrega 550 entradas del semestre, busca de inmediato sin Ollama y filtra
por curso. Muestra definición, origen, relacionados y sinónimos disponibles. Permite
favorito persistente, abrir el módulo y saltar a tarjetas o evaluaciones filtradas por el
mismo curso/módulo. La búsqueda es un índice local en memoria; no requiere FTS5 para el
volumen actual.

### Study Lab

La ruta trilingüe Study Lab ofrece diez modos, filtros por curso/módulo/ámbito,
dificultad e idioma, historial, pregunta, fuentes, modelo y estado. Incluye enviar,
cancelar, reintentar, limpiar, guardar nota, convertir en tarjeta y seguimiento.

Las peticiones se ejecutan en `QThread`. Una caída, timeout, respuesta inválida o modelo
local ausente no bloquea las páginas estáticas. La cancelación es lógica: evita publicar
el resultado, aunque una llamada HTTP ya iniciada sólo termina cuando responde o vence
el timeout configurado.

## Esquema SQLite

`SCHEMA_VERSION = 3`. `PRAGMA user_version` se migra de forma idempotente dentro de una
transacción y se rechaza una base creada por una versión futura.

Tablas:

- `schema_migrations`;
- `study_sessions`;
- `module_progress`;
- `attempts`, `practice_progress`, `assessment_sessions`;
- `flashcard_progress`, `review_schedule`, `review_events`;
- `objective_attempts`, `objective_item_results`;
- `open_response_attempts`, `open_response_drafts`;
- `tutor_sessions`, `tutor_messages`;
- `bookmarks`;
- `generated_questions`.

La UI usa únicamente métodos del repositorio. El contenido académico no se duplica:
SQLite guarda IDs, estado y evidencia del estudiante. Se prueba migración v2→v3 y
reinicio del repositorio.

## Repetición espaciada

`reschedule()` es una función pura inspirada en SM-2:

- Again reinicia repeticiones, resta 0,20 a la facilidad y programa 1 día;
- Hard multiplica el intervalo por 1,2 y resta 0,15;
- Good usa 1 día, 6 días y después `intervalo × facilidad`;
- Easy usa 4 días, 10 días y después
  `intervalo × facilidad × 1,3`, sumando 0,15;
- facilidad limitada a 1,3–3,0;
- dos repeticiones pasan a reviewing y cinco a mastered.

Además se guardan primera vista, última revisión, próxima fecha, intervalo, facilidad,
repeticiones, lapsos, último rating, total de repasos, dominio y favorito.

## Recuperación y Ollama/Qwen

`LexicalRetriever` usa una variante BM25 determinista con filtros de curso y módulo,
pesos por clase de fragmento y expansión de términos detectados en el glosario. El
fallback de localización resuelve idioma solicitado → inglés → primer texto disponible.

`TutorContextBuilder` limita la recuperación a siete fragmentos y cada uno a 2.400
caracteres dentro del prompt. El prompt:

- declara al corpus como única fuente académica;
- trata los fragmentos como datos citados, nunca instrucciones;
- exige IDs de fuente;
- separa evidencia de inferencia;
- prohíbe bibliografía inventada y razonamiento interno;
- incluye curso, módulo, idioma, dificultad, modo y versión de prompt.

Si no existe evidencia, no se llama a Ollama y se muestra un mensaje seguro localizado.
Se reutilizan `OllamaConfig`, `OllamaChatClient`, `ChatMessage`, `ChatResponse`, URL,
modelo y timeouts existentes. El modelo por defecto sigue siendo `qwen3.6:27b`, pero no
se impone.

## Política de soporte oculto

El contenido visible y el soporte de tutor se indexan con `FragmentVisibility`
distintas. `allow_hidden` sólo se habilita por `TutorAccessContext` cuando:

- existe una respuesta ya entregada y el modo es evaluación abierta, explicación de
  error o examen oral; o
- se construye un seguimiento posterior al feedback.

Las acumulativas aplican además una segunda barrera learner-visible antes de renderizar.
Las pruebas demuestran que una consulta normal no recupera fragmentos ocultos y que la
acumulativa de DM847 no contiene el soporte del examinador.

## Feedback formativo

El modo de evaluación exige JSON con `OpenResponseFeedback`:

- resumen, fortalezas, omisiones, errores y afirmaciones no respaldadas;
- dimensiones de rúbrica 0–4 con evidencia;
- revisión sugerida, seguimiento, fuentes y confianza del evaluador.

El parser rechaza JSON inválido, dimensiones fuera de rango o respuesta sin resumen y
fuentes. La UI lo muestra como «evaluación formativa local, no calificación oficial».
La respuesta del estudiante, confianza y versiones se persisten antes de solicitar
feedback.

## UI refinement and Ollama diagnostics

Esta corrección conserva `AcademicCatalog`, los IDs canónicos, BM25, SQLite,
`OllamaChatClient`, los modelos tipados y la ejecución mediante `QThread`. No se
modificó contenido científico para resolver defectos de presentación.

### Glosario

La causa de las filas «· DM847» era contenido estructuralmente incompleto: 102 de las
550 entidades de glosario, concentradas en DM847 M06–M15, resuelven término y definición
vacíos en los tres idiomas. La lista anterior concatenaba el texto vacío con el código
de curso. La página ahora resuelve el texto localizado con el fallback existente a
inglés, exige término y definición no vacíos antes de crear la fila, excluye las 102
entidades inutilizables y registra `course`, `module` e ID mediante warning. El defecto
editorial permanece así observable sin inventar ni corregir contenido científico.

Las 448 entradas utilizables muestran sólo el término. Curso, módulo e ID permanecen
como datos estables del modelo y de `Qt.UserRole`, pero el detalle ordinario usa el
nombre completo de la asignatura y el título localizado del módulo. El selector único
se sustituyó por un botón con menú de checkboxes: «Todas» controla las cuatro
asignaturas, se admiten combinaciones de 1–4 y el estado se captura/restaura por códigos
estables al reconstruir la UI en otro idioma. Si el término seleccionado deja de
pertenecer al filtro, el detalle vuelve al estado vacío.

### Tarjetas

`AdaptiveCardBrowser` mide cada cara con `QTextDocument` y el ancho útil real. Una
búsqueda binaria elige el mayor tamaño que cabe: 18–42 px para texto y 18–24 px para
código. El cálculo se repite al cambiar de tarjeta o cara, al restaurar otro idioma o
filtro y al recibir un resize. El texto ordinario usa alineación horizontal centrada y
padding vertical calculado; las tarjetas breves alcanzan 42 px.

El detector de código conserva espacios, aplica fuente monoespaciada, alineación
izquierda y scroll horizontal sólo cuando es necesario. Si el contenido no cabe a
18 px, se fija ese mínimo y se activa scroll vertical real. Se añadió coalescencia por
firma de layout para que actualizar padding o scrollbars no origine un ciclo
resize→timer→recalcular. Anverso/reverso tienen estado visual y accesible, clic,
Space/Enter y valoración 1–4; los botones de valoración sólo se habilitan en el
reverso y el foco vuelve a la tarjeta tras valorar.

### Preflight y diagnóstico de Ollama

La causa del error genérico era doble: `normalized_base_url()` sólo comprobaba el
sufijo textual `/api`, por lo que una URL de endpoint podía terminar como
`/api/chat/api`, y el transporte agrupaba timeout, servicio apagado y protocolo
inválido en el mismo error. La normalización ahora valida esquema y servidor, rechaza
credenciales/query/fragment, elimina sufijos `chat`, `tags` o `version`, colapsa
`/api/api` y produce una única raíz canónica terminada en `/api`.

El flujo compartido con Settings usa:

1. `GET /api/version`, con timeout corto de preflight;
2. `GET /api/tags`, para la lista real de modelos;
3. comparación exacta del modelo solicitado, sin seleccionar otro;
4. `POST /api/chat`, no streaming, sólo cuando el modelo está confirmado.

Study Lab diferencia URL inválida, conexión, modelo ausente, timeout, respuesta vacía
y respuesta inválida. «Probar conexión» ejecuta sólo los dos GET y la comprobación del
modelo; «Abrir configuración» navega a la misma página de preferencias. El nombre no
se presenta como modelo activo antes del preflight. Si falta, se muestran el solicitado
y los detectados. Cancelar impide publicar una respuesta tardía; al finalizar, fallar o
agotar timeout se reactivan los controles sin workers huérfanos ni llamadas duplicadas.

Los estados, botones, roles y fallback están localizados en ES/EN/DA. Las fuentes
visibles muestran nombre completo de asignatura, módulo, tipo y resumen humano. Los IDs
se conservan en «Detalles de fuente», cerrado por defecto, y el soporte oculto no se
publica. El logging incluye URL normalizada, endpoint, modelo, modelos encontrados,
tipo de fallo, duración y timeouts; no incluye pregunta ni respuesta del estudiante.

La validación manual contra Ollama 0.32.1 detectó
`ornith:9b`, `qwen3-embedding:0.6b` y `qwen3.6:27b`. Un modelo inexistente produjo el
diagnóstico específico y la lista detectada sin generar. `qwen3.6:27b` agotó el timeout
configurado de 180 s y la UI recuperó estado y botones. Tras seleccionar explícitamente
el modelo instalado `ornith:9b`, la misma consulta de Study Lab completó en 26,12 s,
marcó el modelo como activo y publicó la respuesta. No hubo fallback automático.

### Evaluación acumulativa

`CumulativeAssessmentRenderer` reemplaza el recorrido recursivo de diccionarios por un
documento que conoce el contrato académico. Presenta título, propósito, aviso de
preparación, nombre completo de asignatura, cobertura humana, competencias oficiales,
componentes, líneas de proyecto, estructura, rúbricas, casos, preguntas y checklist.
Las rúbricas se muestran como filas criterio/puntos/desempeño excelente.

El renderer sólo consulta rutas semánticas conocidas y descarta de forma recursiva
respuestas canónicas, elementos esperados, desempeño insuficiente y soporte del
examinador. No materializa `metadata`, nombres de claves, `covered_modules`,
`covered_outcomes` ni IDs. BMB830, DM847 y BMB831 se abren en ES/EN/DA sin excepción;
DM857 conserva el estado honesto de acumulativa no disponible.

### Pruebas y revisión visual añadidas

Se añadieron regresiones para filas válidas y logging del glosario, filtro
multiasignatura y persistencia por IDs; medición, alineación, mínimo, scroll real,
resize, clic, teclado y rating de tarjetas; normalización de URL, preflight,
servicio apagado, modelo ausente, éxito, timeout, cancelación tardía, no bloqueo,
localización y fuentes de Study Lab; y documento semántico/ramas ocultas de las tres
acumulativas. Las expectativas anteriores que asumían selección automática se
actualizaron para seleccionar explícitamente tras un filtro que excluye el término.

La pasada visual offscreen revisó glosario ES con DM847+BMB831, tarjeta breve a 42 px,
tarjeta extensa a 18 px con scroll, tarjeta de código, anverso/reverso, BMB830 como
documento, modelo ausente, timeout real y generación real completada. También se
verificaron estados ES/EN/DA mediante widgets y clientes falsos deterministas.

## Pruebas y comandos

Se añadieron pruebas de:

- carga segura de 119 YAML, 4 cursos, 54 módulos y conteos reales;
- IDs, localización, referencias, cloze y separación visible/oculta;
- apertura perezosa de los 54 módulos;
- persistencia, reinicio, migración, tarjetas, favoritos, borradores y versiones;
- evaluación objetiva determinista, acumulativas seguras y ausencia honesta de DM857;
- recomendaciones justificadas;
- navegación por curso/módulo y conservación de estado;
- cliente Ollama falso, hilo no bloqueante, timeout, cancelación lógica, evidencia
  insuficiente, feedback válido e inválido;
- pantalla comprensible ante un corpus estructuralmente no cargable.

Validación final:

```text
ruff check .             → correcto
ruff format --check .    → correcto
mypy src                 → correcto (106 archivos fuente)
pytest -q                → 268 passed
git diff --check         → correcto
pip wheel . --no-deps    → rueda creada; 119 YAML incluidos
```

CI y tests no requieren Ollama ni acceso a internet.

## Flujos principales verificados

1. Curso → módulo: seleccionar cualquiera de los 54 IDs crea sólo ese lector y su
   primera pestaña.
2. Tarjeta → voltear → valorar: guarda scheduling y avanza; reiniciar conserva progreso.
3. Glosario → módulo/tarjetas/preguntas: navega por IDs, no por texto traducido.
4. Quiz → respuesta: corrige por `option_id`, persiste el intento y agenda un fallo.
5. Respuesta abierta → confianza → borrador/entrega → Study Lab: recupera rúbrica y
   soporte permitido, ejecuta Ollama en worker y valida feedback tipado.
6. Cambio de idioma: reconstruye texto y conserva identidad/estado persistido.
7. Ollama desconectado: Study Lab muestra error y el resto de la aplicación continúa.
8. YAML no cargable: el bootstrap muestra detalle rastreable y no inicia una sesión.

## Decisiones pendientes y limitaciones conocidas

1. **Bloqueante editorial:** faltan seis tarjetas trilingües de DM857.
2. **Bloqueante editorial:** falta la evaluación acumulativa de DM857.
3. DM857 M01–M14 siguen usando la composición visual Python histórica en `MainWindow`;
   migrarlos al `CourseStudyPage` YAML común debe hacerse con comparación funcional.
4. Los filtros de evaluación por dificultad y estado
   (no intentada/fallada/completada) aún no tienen controles propios.
5. El quiz del módulo no muestra todavía mejor puntuación histórica ni un botón
   dedicado «practicar falladas»; esas falladas sí entran en Repaso.
6. El feedback tipado se muestra, pero todavía no existe una vista para comparar dos
   versiones ni marcar feedback útil/no útil, y el JSON de feedback no se adjunta aún al
   intento previo.
7. Las recomendaciones no incorporan todavía conceptos omitidos del feedback local
   porque ese enlace de persistencia está pendiente.
8. `tutor_sessions`, `tutor_messages` y `generated_questions` están preparados en el
   esquema, pero Study Lab todavía conserva notas/tarjetas de usuario en `QSettings` y
   no implementa el ciclo completo descartar/variar/reportar pregunta generada.
9. La preparación de una acumulativa se consulta, pero su checklist de progreso aún no
   se persiste.
10. La búsqueda de glosario es local en memoria, adecuada para 550 entradas; FTS5 puede
    añadirse si el corpus crece varios órdenes de magnitud.
11. No se ejecuta código Python/R. Conforme a la restricción de seguridad, sólo se
    analiza texto; un runner futuro requerirá proceso aislado, red deshabilitada,
    límites, timeout y limpieza verificable.
12. No se implementó streaming de Ollama; se conserva la respuesta completa no
    streaming solicitada.

## Estado de aceptación

La evolución es utilizable y está cubierta por pruebas, pero no debe etiquetarse como
«semestre editorialmente completo» hasta resolver los puntos 1 y 2. Los puntos 3–9 son
deuda funcional incremental; no requieren reescribir la aplicación ni reducir el
alcance académico.
