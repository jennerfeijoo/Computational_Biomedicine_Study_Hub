"""DM857 pilot laboratory: reliable physiological measurement summaries."""

from __future__ import annotations

from ...i18n.locales import AppLocale
from ...learning.computational_labs import (
    ComputationalLab,
    LabStage,
    LabTask,
    LabTaskKind,
    LocalizedText,
)


def _text(es: str, en: str, da: str) -> LocalizedText:
    return LocalizedText(
        {
            AppLocale.SPANISH_SPAIN: es,
            AppLocale.ENGLISH: en,
            AppLocale.DANISH_DENMARK: da,
        }
    )


_IMPLEMENT_STARTER = '''def summarize_measurements(values, lower, upper):
    """Return (valid_count, invalid_count, rounded_mean)."""
    # Define the input contract before writing the loop.
    # Boolean values must not be treated as physiological measurements.
    raise NotImplementedError
'''

_IMPLEMENT_CHECKS = """
print(summarize_measurements([72, 80, 250, None, 60], 40, 220))
print(summarize_measurements([40, 60, 20], 40, 60))
"""

_EDGE_CHECKS = """
assert summarize_measurements([], 40, 220) == (0, 0, None)
assert summarize_measurements([True, False, 50], 40, 220) == (1, 2, 50.0)
assert summarize_measurements([39.9, 40, 220, 220.1], 40, 220) == (2, 2, 130.0)
try:
    summarize_measurements([70], 220, 40)
except ValueError:
    pass
else:
    raise AssertionError("lower > upper must raise ValueError")
print("edge cases passed")
"""


DM857_LAB_01 = ComputationalLab(
    lab_id="dm857.lab01.measurement-contracts",
    course_code="DM857",
    version="1.0.0",
    title=_text(
        "Laboratorio 1: mediciones fisiológicas confiables",
        "Laboratory 1: reliable physiological measurements",
        "Laboratorium 1: pålidelige fysiologiske målinger",
    ),
    research_question=_text(
        "¿Cómo transformar una lista de mediciones fisiológicas potencialmente sucias en un resumen confiable y defendible?",
        "How can a potentially dirty list of physiological measurements be transformed into a reliable, defensible summary?",
        "Hvordan kan en muligvis uren liste af fysiologiske målinger omdannes til et pålideligt og forsvarligt resumé?",
    ),
    disclaimer=_text(
        "Preparación interna basada en los resultados de aprendizaje de DM857. No reproduce una hoja oficial de laboratorio de SDU.",
        "Internal preparation based on DM857 learning outcomes. It does not reproduce an official SDU laboratory sheet.",
        "Intern forberedelse baseret på læringsmålene i DM857. Den gengiver ikke et officielt SDU-laboratorieark.",
    ),
    data_provenance=_text(
        "Los valores son sintéticos y representan mediciones fisiológicas genéricas. No proceden de pacientes y no deben utilizarse clínicamente.",
        "The values are synthetic and represent generic physiological measurements. They are not patient data and must not be used clinically.",
        "Værdierne er syntetiske og repræsenterer generiske fysiologiske målinger. De er ikke patientdata og må ikke bruges klinisk.",
    ),
    objectives=(
        (
            "dm857.lab01.contract",
            _text(
                "Definir un contrato de entrada explícito para datos biomédicos heterogéneos.",
                "Define an explicit input contract for heterogeneous biomedical data.",
                "Definér en eksplicit inputkontrakt for heterogene biomedicinske data.",
            ),
        ),
        (
            "dm857.lab01.control-flow",
            _text(
                "Implementar validación mediante tipos, condicionales, iteración y funciones.",
                "Implement validation using types, conditionals, iteration, and functions.",
                "Implementér validering med typer, betingelser, iteration og funktioner.",
            ),
        ),
        (
            "dm857.lab01.testing",
            _text(
                "Comprobar casos normales, límites y entradas inválidas de forma reproducible.",
                "Check normal, boundary, and invalid inputs reproducibly.",
                "Kontrollér normale, grænse- og ugyldige input reproducerbart.",
            ),
        ),
        (
            "dm857.lab01.interpretation",
            _text(
                "Interpretar el resumen sin convertir una regla computacional en una conclusión clínica.",
                "Interpret the summary without turning a computational rule into a clinical conclusion.",
                "Fortolk resuméet uden at gøre en beregningsregel til en klinisk konklusion.",
            ),
        ),
    ),
    prerequisites=(
        _text(
            "Variables, listas, comparaciones y operadores booleanos.",
            "Variables, lists, comparisons, and Boolean operators.",
            "Variabler, lister, sammenligninger og booleske operatorer.",
        ),
        _text(
            "Definición y llamada de funciones sencillas en Python.",
            "Defining and calling simple Python functions.",
            "Definition og kald af simple Python-funktioner.",
        ),
        _text(
            "Diferencia entre una regla de calidad de datos y una interpretación biomédica.",
            "The difference between a data-quality rule and a biomedical interpretation.",
            "Forskellen mellem en datakvalitetsregel og en biomedicinsk fortolkning.",
        ),
    ),
    tasks=(
        LabTask(
            task_id="dm857.lab01.prepare.contract",
            stage=LabStage.PREPARE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Contrato de entrada", "Input contract", "Inputkontrakt"),
            instructions=_text(
                "Antes de programar, escribe qué entradas aceptarás, qué valores considerarás válidos y qué debe ocurrir cuando el límite inferior sea mayor que el superior.",
                "Before coding, state which inputs you will accept, which values count as valid, and what must happen when the lower bound exceeds the upper bound.",
                "Før du programmerer, skal du angive, hvilke input du accepterer, hvilke værdier der er gyldige, og hvad der skal ske, når den nedre grænse er større end den øvre.",
            ),
            mentor_notes=_text(
                "Pregunta primero por la unidad analítica, el tratamiento de bool, None y cadenas, y si los límites son inclusivos. No proporciones todavía código.",
                "Ask first about the analytic unit, treatment of bool, None, and strings, and whether limits are inclusive. Do not provide code yet.",
                "Spørg først til analyseenheden, håndtering af bool, None og strenge, og om grænserne er inklusive. Giv endnu ikke kode.",
            ),
            objective_ids=("dm857.lab01.contract",),
            estimated_minutes=12,
        ),
        LabTask(
            task_id="dm857.lab01.investigate.prediction",
            stage=LabStage.INVESTIGATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Predicción manual", "Manual prediction", "Manuel forudsigelse"),
            instructions=_text(
                "Para [72, 80, 250, None, 60] con límites inclusivos 40–220, predice el número de valores válidos, inválidos y la media de los válidos. Explica cada clasificación.",
                "For [72, 80, 250, None, 60] with inclusive limits 40–220, predict valid count, invalid count, and the mean of valid values. Explain each classification.",
                "For [72, 80, 250, None, 60] med inklusive grænser 40–220 skal du forudsige antal gyldige og ugyldige værdier samt middelværdien af de gyldige. Forklar hver klassifikation.",
            ),
            mentor_notes=_text(
                "Comprueba que la respuesta distingue validación de cálculo y que excluye 250 y None antes de calcular la media.",
                "Check that the response separates validation from calculation and excludes 250 and None before computing the mean.",
                "Kontrollér, at svaret adskiller validering fra beregning og udelukker 250 og None før middelværdien beregnes.",
            ),
            objective_ids=("dm857.lab01.contract", "dm857.lab01.interpretation"),
            estimated_minutes=10,
        ),
        LabTask(
            task_id="dm857.lab01.implement.function",
            stage=LabStage.IMPLEMENT,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Implementación modular", "Modular implementation", "Modulær implementering"
            ),
            instructions=_text(
                "Implementa summarize_measurements. Debe devolver (válidos, inválidos, media_redondeada), usar límites inclusivos, excluir booleanos y devolver None cuando no haya valores válidos.",
                "Implement summarize_measurements. It must return (valid, invalid, rounded_mean), use inclusive limits, exclude Boolean values, and return None when no valid values exist.",
                "Implementér summarize_measurements. Den skal returnere (gyldige, ugyldige, afrundet_middel), bruge inklusive grænser, udelukke booleske værdier og returnere None, når ingen gyldige værdier findes.",
            ),
            mentor_notes=_text(
                "Usa preguntas sobre invariantes, acumulación y separación de validación/cálculo. Ofrece pseudocódigo solo después de una explicación del estudiante.",
                "Use questions about invariants, accumulation, and separating validation from calculation. Offer pseudocode only after the learner explains a plan.",
                "Brug spørgsmål om invarianter, akkumulering og adskillelse af validering og beregning. Giv kun pseudokode efter elevens egen plan.",
            ),
            objective_ids=("dm857.lab01.control-flow",),
            estimated_minutes=30,
            starter_response=_IMPLEMENT_STARTER,
            verification_source=_IMPLEMENT_CHECKS,
            expected_output="(3, 2, 70.67)\n(2, 1, 50.0)",
        ),
        LabTask(
            task_id="dm857.lab01.check.edge-cases",
            stage=LabStage.CHECK,
            kind=LabTaskKind.PYTHON,
            title=_text("Casos límite", "Boundary cases", "Grænsetilfælde"),
            instructions=_text(
                "Reutiliza y fortalece la función anterior. El checkpoint comprueba lista vacía, booleanos, límites exactos y un intervalo invertido. No se muestran las pruebas internas.",
                "Reuse and strengthen the previous function. The checkpoint checks an empty list, Boolean values, exact boundaries, and a reversed interval. Internal tests are not shown.",
                "Genbrug og styrk den forrige funktion. Checkpointet kontrollerer en tom liste, booleske værdier, nøjagtige grænser og et omvendt interval. De interne tests vises ikke.",
            ),
            mentor_notes=_text(
                "Cuando falle, pide al estudiante que formule primero qué caso límite contradice su contrato. No reveles el código de verificación.",
                "When it fails, ask the learner to identify which boundary case contradicts the contract. Do not reveal verification code.",
                "Ved fejl skal du først bede den studerende identificere, hvilket grænsetilfælde der strider mod kontrakten. Afslør ikke verifikationskoden.",
            ),
            objective_ids=("dm857.lab01.control-flow", "dm857.lab01.testing"),
            estimated_minutes=22,
            verification_source=_EDGE_CHECKS,
            expected_output="edge cases passed",
            seed_from_task_id="dm857.lab01.implement.function",
        ),
        LabTask(
            task_id="dm857.lab01.interpret.result",
            stage=LabStage.INTERPRET,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Interpretación biomédica", "Biomedical interpretation", "Biomedicinsk fortolkning"
            ),
            instructions=_text(
                "Interpreta el resumen (3 válidos, 2 inválidos, media 70.67). Explica qué afirma el programa, qué no demuestra clínicamente y qué metadatos necesitarías antes de usarlo en una investigación.",
                "Interpret the summary (3 valid, 2 invalid, mean 70.67). Explain what the program establishes, what it does not establish clinically, and which metadata would be needed before research use.",
                "Fortolk resuméet (3 gyldige, 2 ugyldige, middel 70,67). Forklar, hvad programmet fastslår, hvad det ikke dokumenterer klinisk, og hvilke metadata der kræves før forskningsbrug.",
            ),
            mentor_notes=_text(
                "Exige separar resultado computacional, calidad de datos y significado clínico. Pregunta por unidades, dispositivo, población y contexto temporal.",
                "Require separation of computational result, data quality, and clinical meaning. Ask about units, device, population, and temporal context.",
                "Kræv adskillelse af beregningsresultat, datakvalitet og klinisk betydning. Spørg til enheder, udstyr, population og tidsmæssig kontekst.",
            ),
            objective_ids=("dm857.lab01.interpretation",),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm857.lab01.defend.design",
            stage=LabStage.DEFEND,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Defensa de diseño", "Design defence", "Forsvar af design"),
            instructions=_text(
                "Defiende dos decisiones de diseño de tu función y compara una alternativa. Incluye al menos una decisión sobre errores y otra sobre el valor devuelto.",
                "Defend two design decisions in your function and compare one alternative. Include at least one error-handling decision and one return-value decision.",
                "Forsvar to designbeslutninger i din funktion og sammenlign med et alternativ. Medtag mindst én beslutning om fejlhåndtering og én om returværdien.",
            ),
            mentor_notes=_text(
                "Actúa como examinador: pide una justificación, una alternativa y una consecuencia. Detecta afirmaciones memorizadas sin relación con el código escrito.",
                "Act as an examiner: request a justification, an alternative, and a consequence. Detect memorised claims unrelated to the submitted code.",
                "Opfør dig som eksaminator: bed om en begrundelse, et alternativ og en konsekvens. Opdag indlærte påstande uden forbindelse til den indsendte kode.",
            ),
            objective_ids=("dm857.lab01.contract", "dm857.lab01.control-flow"),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm857.lab01.consolidate.reflection",
            stage=LabStage.CONSOLIDATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Reflexión de error", "Error reflection", "Fejlrefleksion"),
            instructions=_text(
                "Describe el error más importante encontrado, cómo lo detectaste, qué cambio lo corrigió y qué prueba evitará que reaparezca.",
                "Describe the most important error encountered, how it was detected, which change corrected it, and which test will prevent recurrence.",
                "Beskriv den vigtigste fejl, hvordan den blev opdaget, hvilken ændring der rettede den, og hvilken test der vil forhindre gentagelse.",
            ),
            mentor_notes=_text(
                "No aceptes una reflexión genérica. Solicita vínculo explícito entre error, evidencia, corrección y prueba de regresión.",
                "Do not accept a generic reflection. Require an explicit link between error, evidence, correction, and regression test.",
                "Accepter ikke en generisk refleksion. Kræv en tydelig forbindelse mellem fejl, evidens, rettelse og regressionstest.",
            ),
            objective_ids=("dm857.lab01.testing", "dm857.lab01.interpretation"),
            estimated_minutes=12,
        ),
    ),
    estimated_minutes=120,
)

__all__ = ["DM857_LAB_01"]
