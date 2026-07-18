"""Authored objective-question bank for randomized DM857 module 1 sessions."""

from __future__ import annotations

from ...learning.activity_types import ActivityType
from ..models import AssessmentItem

OBJECTIVE_QUESTION_BANK: tuple[AssessmentItem, ...] = (
    AssessmentItem(
        item_id="dm857.m01.bank.001",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué secuencia representa mejor el paso desde una situación real hasta código ejecutable?",
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
        item_id="dm857.m01.bank.002",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es la función principal de un modelo computacional en este módulo?",
        options=(
            "Conservar las variables y relaciones relevantes del problema",
            "Copiar todos los detalles de la situación real",
            "Sustituir las pruebas del programa",
            "Elegir automáticamente la sintaxis de Python",
        ),
        correct_answers=("Conservar las variables y relaciones relevantes del problema",),
        explanation=(
            "El modelo abstrae la situación y conserva únicamente la información necesaria "
            "para producir una respuesta verificable."
        ),
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.003",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="Una expresión es código que Python puede evaluar para producir un valor.",
        options=("Verdadero", "Falso"),
        correct_answers=("Verdadero",),
        explanation="Una expresión combina elementos evaluables y produce un valor concreto.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.004",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el valor y el tipo de 9 / 3 en Python?",
        options=("3.0, float", "3, int", "3.0, int", "9/3, str"),
        correct_answers=("3.0, float",),
        explanation="El operador / realiza división real y devuelve float incluso si es exacta.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.005",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el resultado de 9 // 4?",
        options=("2", "2.25", "3", "1"),
        correct_answers=("2",),
        explanation="// aplica división entera hacia abajo; 9 dividido para 4 tiene cociente 2.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.006",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="input() devuelve un entero cuando el usuario escribe únicamente dígitos.",
        options=("Verdadero", "Falso"),
        correct_answers=("Falso",),
        explanation="input() devuelve str; la conversión numérica debe realizarse explícitamente.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.007",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué produce int(4.9)?",
        options=("4", "5", "4.9", "TypeError"),
        correct_answers=("4",),
        explanation="int() elimina la parte fraccionaria hacia cero; no realiza redondeo convencional.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.008",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="El operador ^ representa exponenciación en Python.",
        options=("Verdadero", "Falso"),
        correct_answers=("Falso",),
        explanation="La exponenciación se escribe con **; ^ es una operación bit a bit.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.009",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cómo debe interpretarse x = x + 1?",
        options=(
            "Se evalúa x + 1 y después se reasigna x",
            "Es una igualdad matemática imposible",
            "Se incrementa x antes de evaluar la expresión",
            "Se crea una segunda variable llamada x",
        ),
        correct_answers=("Se evalúa x + 1 y después se reasigna x",),
        explanation=(
            "La asignación evalúa completamente el lado derecho usando el estado actual y "
            "después actualiza el nombre de la izquierda."
        ),
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.010",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué imprime el código x = 4; y = x + 2; x = 10; print(y)?",
        options=("6", "12", "10", "4"),
        correct_answers=("6",),
        explanation="y almacena 6 antes de la reasignación de x y no se recalcula automáticamente.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.011",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="Reasignar x actualiza automáticamente cualquier variable calculada previamente con x.",
        options=("Verdadero", "Falso"),
        correct_answers=("Falso",),
        explanation="Las variables conservan el valor asignado; no mantienen dependencias automáticas.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.012",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué ocurre al ejecutar '12' + 3?",
        options=(
            "Se produce TypeError por combinar str e int",
            "Se obtiene 15",
            "Se obtiene '123'",
            "Se produce SyntaxError",
        ),
        correct_answers=("Se produce TypeError por combinar str e int",),
        explanation="La suma directa entre str e int no está definida; debe decidirse la conversión adecuada.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.013",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál situación describe un error lógico?",
        options=(
            "El programa termina sin excepción pero usa 100 en vez de 1000 al convertir mL a µL",
            "Python no puede interpretar un paréntesis sin cerrar",
            "El programa divide entre cero",
            "Se intenta sumar str e int",
        ),
        correct_answers=(
            "El programa termina sin excepción pero usa 100 en vez de 1000 al convertir mL a µL",
        ),
        explanation=(
            "Un error lógico permite ejecutar el programa, pero el resultado no satisface la especificación."
        ),
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.014",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué información mínima convierte una ejecución en una prueba?",
        options=(
            "Entrada, resultado esperado y criterio de comparación",
            "Solo el código fuente",
            "Una entrada elegida al azar sin resultado esperado",
            "La ausencia de mensajes de error",
        ),
        correct_answers=("Entrada, resultado esperado y criterio de comparación",),
        explanation="Una prueba compara un resultado observado con uno esperado para una entrada concreta.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.015",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="La ausencia de excepciones demuestra que un programa es correcto.",
        options=("Verdadero", "Falso"),
        correct_answers=("Falso",),
        explanation="El programa puede contener errores lógicos aunque termine sin excepciones.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.016",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Qué nombre reduce mejor el riesgo de confundir unidades?",
        options=("total_volume_ul", "value", "number", "x"),
        correct_answers=("total_volume_ul",),
        explanation="Incluir el significado y la unidad documenta el modelo y ayuda a detectar inconsistencias.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.017",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el resultado de 8 + 4 * 3?",
        options=("20", "36", "24", "12"),
        correct_answers=("20",),
        explanation="La multiplicación tiene mayor precedencia: 4 * 3 = 12 y después 8 + 12 = 20.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.018",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Cuál es el resultado de (8 + 4) * 3?",
        options=("36", "20", "24", "15"),
        correct_answers=("36",),
        explanation="Los paréntesis obligan a evaluar primero 8 + 4 y después multiplicar por 3.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.019",
        activity_type=ActivityType.TRUE_FALSE,
        prompt="Una variable puede asociarse con valores de tipos diferentes en momentos distintos.",
        options=("Verdadero", "Falso"),
        correct_answers=("Verdadero",),
        explanation="Python usa tipado dinámico, aunque cada valor posee un tipo definido.",
    ),
    AssessmentItem(
        item_id="dm857.m01.bank.020",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt="¿Por qué conviene convertir a int al final del cálculo de lecturas útiles?",
        options=(
            "Porque el resultado representa un conteo y antes puede requerir aritmética con float",
            "Porque int siempre mejora la precisión",
            "Porque Python no permite multiplicar int por float",
            "Porque todos los datos biomédicos deben ser enteros",
        ),
        correct_answers=(
            "Porque el resultado representa un conteo y antes puede requerir aritmética con float",
        ),
        explanation=(
            "La conversión debe responder al significado del resultado; durante el cálculo puede ser "
            "necesario conservar la parte decimal."
        ),
    ),
)

__all__ = ["OBJECTIVE_QUESTION_BANK"]
