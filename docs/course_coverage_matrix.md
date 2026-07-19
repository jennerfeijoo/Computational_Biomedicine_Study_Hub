# Matriz de cobertura académica

Fecha de revisión: 2026-07-19.

Esta matriz relaciona la descripción oficial de DM857 con artefactos que existen en el
catálogo. Los IDs son independientes del idioma. Cuando una celda contiene un rango, todos
los elementos del rango existen; se indica un elemento representativo para que la cadena
pueda inspeccionarse sin convertir la tabla en un inventario de cientos de filas.

Fuente oficial:
[DM857 — Course Description, ODIN/SDU](https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=DM857&lang=en).

## DM857

| Resultado oficial | Módulo | Objetivo | Concepto | Ejemplo resuelto | Práctica | Evaluación authored / banco objetivo |
|---|---|---|---|---|---|---|
| Diseñar un modelo para un problema concreto | `dm857.m01` | `m01.o1` | `problem-model-algorithm-program` | `sequencing-yield` | `m01.p01` | `m01.a01` / `dm857.m01.*` |
| Diseñar una estructura de programa que represente el modelo | `dm857.m04` | `m04.o6` | `decomposition-and-composition` | `m04.e5` | `m04.p11` | `dm857.m04.assessment.011` / `dm857.m04.*` |
| Implementar el modelo en Python | `dm857.m01`–`dm857.m08` | `m01.o2`–`m08.o8` | estado, control, funciones y colecciones | 32 ejemplos | `m01.p01`–`m08.p12` | authored de m01–m08 / bancos de m01–m08 |
| Secuencia, valores, tipos y estado | `dm857.m01` | `m01.o2`, `m01.o4` | `expressions-values-types`, `variables-assignment-state` | `sample-volume` | `m01.p02`, `m01.p04` | `m01.a02`, `m01.a04` / `dm857.m01.*` |
| Selección y lógica booleana | `dm857.m02` | `m02.o1`–`m02.o7` | `if-elif-else-control-flow` | `sample-quality-decision` | `m02.p01`–`m02.p10` | `m02.a01`–`m02.a12` / `dm857.m02.*` |
| Repetición | `dm857.m03` | `m03.o1`–`m03.o8` | `while-loop-anatomy`, `for-loop-and-range` | `m03.e01`–`m03.e05` | `m03.p01`–`m03.p12` | `m03.a01`–`m03.a14` / `dm857.m03.*` |
| Subprogramas y programación estructurada | `dm857.m04` | `m04.o1`–`m04.o8` | `definition-call-and-interface`, `contracts-and-documentation` | `m04.e1`–`m04.e5` | `m04.p01`–`m04.p12` | `dm857.m04.assessment.001`–`.014` / banco m04 |
| Listas y secuencias | `dm857.m05`, `dm857.m06` | `m05.o1`–`m06.o8` | `string-sequence-and-immutability`, `ordered-sequences` | `m05.e1`, `m06.e1` | `m05.p01`–`m06.p12` | authored y bancos m05–m06 |
| Mapas y conjuntos | `dm857.m07` | `m07.o1`–`m07.o8` | `mapping-model-and-keys`, `set-algebra` | `frequency-table`, `compare-identifiers` | `m07.p01`–`m07.p12` | authored m07 / banco m07 |
| Entrada/salida, validación y errores | `dm857.m08` | `m08.o1`–`m08.o8` | `open-modes-encoding-context`, `exceptions-and-specificity` | `parse-csv`, `convert-with-context` | `m08.p01`–`m08.p12` | authored m08 / banco m08 |
| Desarrollar soluciones recursivas | `dm857.m09` | `m09.o1`–`m09.o8` | `recursive-contract`, `progress-and-termination` | `factorial`, `flatten` | `m09.p01`–`m09.p12` | authored m09 / banco m09 |
| Estructuras de árbol básicas | `dm857.m10` | `m10.o1`–`m10.o8` | `tree-vocabulary`, `depth-first-traversals` | `binary-preorder`, `breadth-first-levels` | `m10.p01`–`m10.p12` | authored m10 / banco m10 |
| Tipos abstractos de datos | `dm857.m11` | `m11.o1`–`m11.o8` | `adt-interface-contract`, `representation-invariants` | `stack-class`, `stable-priority-queue` | `m11.p01`–`m11.p12` | authored m11 / banco m11 |
| Representación con clases y objetos | `dm857.m12` | `m12.o1`–`m12.o8` | `classes-and-instances`, `composition-inheritance-polymorphism` | `validated-counter`, `composition` | `m12.p01`–`m12.p12` | authored m12 / banco m12 |
| Encontrar y utilizar elementos de bibliotecas | `dm857.m13` | `m13.o1`–`m13.o8` | `documentation-and-api`, `numpy-array-model`, `pandas-tabular-model` | `array-standardization`, `dataframe-filter` | `m13.p01`–`m13.p12` | authored m13 / banco m13 |
| Planificar y ejecutar pruebas | `dm857.m14` | `m14.o1`–`m14.o8` | `tests-as-contracts`, `parametrization-boundaries-exceptions` | `m14.e01`–`m14.e05` | `m14.p01`–`m14.p12` | authored m14 / banco m14 |

## Cobertura transversal y huecos

| Resultado/forma de evaluación | Evidencia actual | Cobertura funcional | Acción |
|---|---|---|---|
| Integrar modelado, implementación, testing e interpretación | Los temas existen en m01, m04, m13 y m14 | No existe un proyecto persistente que los conecte | Añadir evaluación acumulativa/proyecto sin reescribir módulos |
| Preparar informe de proyecto | Hay rúbricas y explicaciones, no flujo de informe | Ausente | Plantilla, hitos, rúbrica y evidencia vinculada a una sesión |
| Presentación y examen oral individual | Existen `ORAL_EXPLANATION` y criterios de tutor | Sólo respuesta textual genérica | Renderer oral, autoevaluación por rúbrica e interfaz opcional de tutor |
| Recuperación y práctica espaciada | Bancos objetivos y prácticas abundantes | Ausente por falta de persistencia/Review | Cola persistente y algoritmo desacoplado |
| Transferencia entre módulos | Actividades authored por módulo | No hay selección acumulativa | Assessments acumulativo y mixto por IDs |

## Cursos aún sin catálogo académico

No se puede construir una relación
`resultado oficial -> módulo -> concepto -> ejemplo -> práctica -> evaluación` para DM847,
BMB830 o BMB831 porque el repositorio sólo contiene su registro y una página de estructura.
Asignarles resultados oficiales o marcar cobertura ahora sería una afirmación no respaldada.

| Curso | Secuencia futura de alto nivel | Condición de entrada al catálogo |
|---|---|---|
| DM847 | secuencias → alineamiento → motivos → HMM → índices → NGS → redes → ómicas → proyecto | resultados oficiales verificados, bundles trilingües, actividades y evaluación |
| BMB830 | R reproducible → datos → descriptiva → probabilidad → inferencia → grupos → regresión → informe | resultados oficiales verificados, datasets con licencia y ejecución R aislada |
| BMB831 | modelos avanzados → FDR → reducción dimensional → clustering → clasificación → Bioconductor → pipelines → proyecto | resultados oficiales verificados, datasets con licencia y ejecución R aislada |

La incorporación de estos cursos debe reutilizar el mismo catálogo abstracto, repositorio de
progreso y registro de renderers. No debe añadir condicionales por código de curso en las
páginas globales.
