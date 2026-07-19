# Auditoría del contenido académico del primer semestre

Fecha de auditoría: 19 de julio de 2026  
Rama: `feat/semester-1-learning-engine`  
Fuente: `academic_content/semester_1/`

## Resumen global

Se revisaron los 119 archivos YAML del semestre mediante `yaml.safe_load`, contando los
elementos almacenados y no sólo los campos declarativos. Después de las correcciones
estructurales descritas abajo, los 119 archivos son sintácticamente válidos y no hay
archivos vacíos.

El corpus contiene las cuatro asignaturas y los 54 módulos esperados, pero contiene
1.338 tarjetas, no 1.344. La diferencia está íntegramente en DM857: sus objetivos por
módulo declaran 15 módulos estándar de 24 tarjetas y dos integradores de 30, que suman
420; el total editorial de 426/1.344 era aritméticamente incompatible con ese desglose.
No existen seis tarjetas adicionales en los archivos. Tampoco existe una evaluación
acumulativa de DM857.

Estos dos déficits requieren autoría académica. No se inventaron tarjetas, soluciones,
rúbricas, fórmulas ni traducciones para forzar los criterios numéricos.

## Archivos revisados

| Grupo | Archivos |
|---|---:|
| Contrato, blueprint y especificaciones globales | 4 |
| Descriptores de asignatura | 4 |
| Módulos | 54 |
| Bancos de tarjetas por módulo | 54 |
| Evaluaciones acumulativas | 3 |
| **Total** | **119** |

Distribución de módulos: DM857 17, DM847 15, BMB830 10 y BMB831 12.

## Conteos reales

| Asignatura | Módulos | Tarjetas reales | Objetivo solicitado | Diferencia | Evaluación acumulativa |
|---|---:|---:|---:|---:|---|
| DM857 | 17 | 420 | 426 | -6 | No |
| DM847 | 15 | 372 | 372 | 0 | Sí |
| BMB830 | 10 | 246 | 246 | 0 | Sí |
| BMB831 | 12 | 300 | 300 | 0 | Sí |
| **Total** | **54** | **1.338** | **1.344** | **-6** | **3 de 4** |

Los 54 archivos de tarjetas tienen un conteo declarado igual a la longitud real de
`cards`. Las 1.338 tarjetas tienen IDs únicos, prefijo de curso y módulo coherente,
anverso y reverso no vacíos, y contenido en español, inglés y danés.

## Errores bloqueantes

### 1. Déficit de seis tarjetas en DM857

- Código del validador: `semester.flashcard_count` y `course.flashcard_count`.
- Evidencia: 420 objetos bajo `cards` para DM857 y 1.338 en todo el semestre.
- Origen declarativo: `flashcard_coverage_plan.yaml` indicaba 426 para DM857 y 1.344
  globales, aunque el desglose por módulo suma 420.
- Impacto: no puede cumplirse el criterio de 1.344 tarjetas sin crear contenido
  académico nuevo.
- Acción requerida: revisión humana que decida qué seis objetivos necesitan cobertura
  adicional y redacte las tarjetas trilingües con IDs nuevos y referencias válidas.

### 2. Evaluación acumulativa de DM857 ausente

- Código del validador: `course.cumulative_missing`.
- Evidencia: no existe `academic_content/semester_1/dm857/assessments/*.yaml`; las otras
  tres asignaturas sí incluyen una evaluación acumulativa.
- Impacto: la página global puede mostrar las tres evaluaciones existentes, pero no una
  evaluación acumulativa canónica de DM857.
- Acción requerida: autoría y revisión académica de propósito, requisitos, rúbrica,
  checklist y preguntas de defensa.

## Advertencias y revisión humana

### Textos visibles disponibles sólo en inglés

Los siguientes campos `metadata.official_format_reference` tienen `en` pero no `es` ni
`da`:

- `bmb830/assessments/bmb830_cumulative_assessment.yaml`
- `bmb831/assessments/bmb831_cumulative_assessment.yaml`
- `dm847/assessments/dm847_cumulative_assessment.yaml`

Se conservaron sin traducción automática porque describen el formato oficial de
evaluación y una traducción semántica debe revisarse académicamente.

### IDs fuente locales reutilizados

Hay 46 IDs de entidades reutilizados en más de un módulo: 37 objetivos con forma local
como `m01.o1` y nueve términos de glosario como `term.provenance`,
`term.normalization`, `term.index`, `term.affine_gap`, `term.traceback`,
`term.progress_measure`, `term.sentinel`, `term.scope` y `term.identity`.

No se eliminaron ni renombraron porque son IDs existentes. La capa académica expone
una identidad cualificada por curso/módulo y obtiene 3.938 identidades de runtime
únicas, manteniendo el ID fuente para trazabilidad y compatibilidad. Para una futura
versión del contrato conviene declarar formalmente si esos IDs son locales o migrarlos
con una tabla explícita de alias.

## Referencias

- Todas las referencias de objetivos usadas por tarjetas resuelven dentro de su módulo.
- Todos los prerrequisitos con forma de ID de módulo apuntan a uno de los 54 módulos.
- Las referencias entre cursos detectadas en prerrequisitos son válidas.
- Once referencias de tarjetas de DM857 M01 apuntaban a dos conceptos inexistentes:
  `statements-input-output-tracing` y `errors-tests-and-evidence`. Ambas eran nombres
  parciales del concepto existente `input-output-and-errors`; se corrigieron sólo las
  referencias, sin cambiar los IDs de tarjeta ni el contenido visible.

## Traducciones

- Todos los títulos y resúmenes de módulo tienen `es`, `en` y `da`.
- Todos los anversos y reversos de tarjeta tienen los tres idiomas.
- El recorrido recursivo de mapas localizados sólo detecta las tres referencias
  oficiales monolingües enumeradas arriba.
- El runtime permite fallback controlado a inglés, pero el validador sigue registrando
  la ausencia para que el fallback no oculte deuda editorial.

## Duplicados

No se detectaron anversos idénticos ni pares con similitud normalizada igual o superior
al 94 % dentro del mismo módulo. Los IDs de las 1.338 tarjetas son globalmente únicos.

## Contrato editorial y material oculto

Los 54 módulos contienen objetivos, conceptos, ejemplos, práctica, banco objetivo,
evaluación abierta, glosario y soporte oculto no vacío, admitiendo los nombres
históricos documentados por la capa de carga. El soporte
`hidden_tutor_support`/`hidden_support`/`hidden_guided_support` se carga en una
estructura separada y no forma parte de las colecciones visibles.

## Correcciones estructurales realizadas

1. Se citaron mecánicamente valores escalares localizados en 116 archivos. Antes de la
   corrección, 102 de los 119 archivos no eran aceptados por `safe_load` por signos de
   interrogación, dos puntos o backticks dentro de valores sin comillas.
2. Se repararon cuatro defectos puntuales: una llave sobrante en BMB831 M05, una llave
   ausente en DM847 M12, un mapa localizado multilínea inválido en una tarjeta de
   DM857 M06 y una lista con backticks sin citar en DM857 M13.
3. Se corrigieron 11 referencias inequívocamente erróneas de tarjetas de DM857 M01 al
   concepto existente `input-output-and-errors`.
4. Se corrigieron los campos declarativos de `flashcard_coverage_plan.yaml` a los
   conteos que realmente resultan de su propio desglose: DM857 420, total 1.338 y
   4.014 pares localizados.
5. Se añadió un normalizador idempotente en
   `scripts/normalize_semester_1_yaml.py`; una segunda ejecución no produce cambios.

Ninguna corrección alteró explicaciones científicas, respuestas correctas, fórmulas,
rúbricas o el significado de las traducciones.

## Resultado

El corpus es cargable y navegable, pero la auditoría editorial no puede declararse
completa mientras falten seis tarjetas y la evaluación acumulativa de DM857. La
integración técnica debe conservar esa limitación visible y no presentar 1.338 como
1.344.
