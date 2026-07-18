"""Extended closed-question bank for DM857 module 1."""

from __future__ import annotations

from ...learning.activity_types import ActivityType
from ..models import AssessmentItem

EXTRA_CLOSED_ASSESSMENT_ITEMS: tuple[AssessmentItem, ...] = (
    AssessmentItem(
        item_id="m01.bank01",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el valor y el tipo de 9 / 3 en Python?",
        options=("3 (int)", "3.0 (float)", "3 (str)", "La expresión genera un error"),
        correct_answers=("3.0 (float)",),
        explanation=(
            "El operador / realiza división real y devuelve float, incluso cuando el resultado "
            "matemático no tiene parte fraccionaria."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank02",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué devuelve int(4.9)?",
        options=("4", "5", "4.9", "ValueError"),
        correct_answers=("4",),
        explanation=(
            "int aplicado a un float elimina la parte fraccionaria hacia cero; no redondea al "
            "entero más cercano."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank03",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="input() devuelve un valor de tipo str aunque el usuario escriba únicamente dígitos.",
        options=("Verdadero", "Falso"),
        correct_answers=("Verdadero",),
        explanation=(
            "input siempre produce texto. Para realizar aritmética se necesita una conversión "
            "explícita, por ejemplo int() o float()."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank04",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué operador representa la exponenciación en Python?",
        options=("**", "^", "//", "%"),
        correct_answers=("**",),
        explanation="Python usa ** para exponenciación; ^ realiza XOR bit a bit.",
    ),
    AssessmentItem(
        item_id="m01.bank05",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="Después de ejecutar x = 5; y = x * 2; x = 8, ¿cuál es el valor de y?",
        options=("10", "16", "8", "No está definido"),
        correct_answers=("10",),
        explanation=(
            "y almacena el resultado calculado cuando x valía 5. Reasignar x después no "
            "recalcula automáticamente y."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank06",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="Un programa que termina sin excepciones está necesariamente correcto.",
        options=("Verdadero", "Falso"),
        correct_answers=("Falso",),
        explanation=(
            "Un error lógico puede producir una ejecución completa y, aun así, una salida que no "
            "satisface la especificación."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank07",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué información convierte una ejecución en una prueba reproducible?",
        options=(
            "Una entrada y un resultado esperado definidos",
            "Solo comprobar que no aparece una excepción",
            "Imprimir muchas variables sin criterio",
            "Ejecutar el programa varias veces con la misma entrada",
        ),
        correct_answers=("Una entrada y un resultado esperado definidos",),
        explanation=(
            "Una prueba compara un resultado observado con un resultado esperado para una entrada "
            "concreta y un criterio de aceptación."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank08",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué nombre de variable comunica mejor que el valor 840 representa microlitros?",
        options=("total_volume_ul", "value", "number", "total"),
        correct_answers=("total_volume_ul",),
        explanation=(
            "Incluir la magnitud y la unidad en el nombre reduce ambigüedad y ayuda a detectar "
            "errores dimensionales."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank09",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el resultado de 8 + 4 * 3?",
        options=("20", "36", "24", "12"),
        correct_answers=("20",),
        explanation=(
            "La multiplicación tiene mayor precedencia que la suma: primero 4 * 3 = 12 y después "
            "8 + 12 = 20."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank10",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el orden correcto desde una situación real hasta código ejecutable?",
        options=(
            "Problema → modelo → algoritmo → programa",
            "Programa → algoritmo → modelo → problema",
            "Modelo → problema → programa → algoritmo",
            "Algoritmo → programa → problema → modelo",
        ),
        correct_answers=("Problema → modelo → algoritmo → programa",),
        explanation=(
            "Primero se delimita el problema, después se construye un modelo, se diseña un "
            "algoritmo y finalmente se implementa como programa."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank11",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué expresión convierte correctamente la cadena '3.5' en un número decimal?",
        options=("float('3.5')", "int('3.5')", "str(3.5)", "'3.5' / 1"),
        correct_answers=("float('3.5')",),
        explanation=(
            "float interpreta una representación textual decimal válida. int('3.5') no acepta "
            "el punto decimal directamente."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank12",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="Una variable puede asociarse con valores de tipos diferentes en momentos distintos.",
        options=("Verdadero", "Falso"),
        correct_answers=("Verdadero",),
        explanation=(
            "Python usa tipado dinámico: el nombre puede reasignarse, aunque cada valor conserva "
            "un tipo concreto."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank13",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el resultado de '3' + '4'?",
        options=("'34'", "7", "7.0", "TypeError"),
        correct_answers=("'34'",),
        explanation=(
            "Ambos operandos son cadenas, por lo que + realiza concatenación y produce la cadena "
            "'34'."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank14",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué expresa x = x + 1 en un programa?",
        options=(
            "Una actualización del estado de x",
            "Una igualdad matemática",
            "Una comparación entre dos valores",
            "La creación obligatoria de un float",
        ),
        correct_answers=("Una actualización del estado de x",),
        explanation=(
            "Se evalúa el lado derecho con el valor actual de x y después se reasigna el nombre x "
            "al resultado."
        ),
    ),
    AssessmentItem(
        item_id="m01.bank15",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el resultado de 17 % 5?",
        options=("2", "3", "3.4", "12"),
        correct_answers=("2",),
        explanation="El operador % devuelve el resto de la división entera: 17 = 3 × 5 + 2.",
    ),
    AssessmentItem(
        item_id="m01.bank16",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt=(
            "Una corrida produce 1_000 lecturas y el 80 % pasa control de calidad. "
            "¿Qué expresión calcula las lecturas útiles?"
        ),
        options=(
            "int(1_000 * 0.80)",
            "1_000 + 0.80",
            "1_000 / 80",
            "str(1_000) * 0.80",
        ),
        correct_answers=("int(1_000 * 0.80)",),
        explanation=(
            "El porcentaje se representa como 0.80, se multiplica por el total y se convierte al "
            "final porque el resultado representa un conteo de lecturas."
        ),
    ),
)
