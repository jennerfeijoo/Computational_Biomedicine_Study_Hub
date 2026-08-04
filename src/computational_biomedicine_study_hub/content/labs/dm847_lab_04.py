"""DM847 laboratory 4: hidden Markov models and probabilistic decoding."""

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


_FORWARD_STARTER = '''import math


def logsumexp(values):
    """Return log(sum(exp(values))) without avoidable underflow."""
    raise NotImplementedError


def validate_model(model):
    """Validate states, initial probabilities, transitions, and emissions."""
    raise NotImplementedError


def forward_log_likelihood(observations, model):
    """Return log P(observations | model) using the Forward algorithm."""
    raise NotImplementedError
'''

_FORWARD_CHECKS = """
model = {
    "states": ("H", "L"),
    "initial": {"H": 0.5, "L": 0.5},
    "transition": {
        "H": {"H": 0.8, "L": 0.2},
        "L": {"H": 0.2, "L": 0.8},
    },
    "emission": {
        "H": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1},
        "L": {"A": 0.4, "C": 0.1, "G": 0.1, "T": 0.4},
    },
}
assert forward_log_likelihood("", model) == 0.0
print(round(forward_log_likelihood("ACGT", model), 6))
print(round(forward_log_likelihood("GGGCAATT", model), 6))
"""

_DECODING_STARTER = '''import math


def logsumexp(values):
    """Return log(sum(exp(values))) without avoidable underflow."""
    raise NotImplementedError


def validate_model(model):
    """Validate states, initial probabilities, transitions, and emissions."""
    raise NotImplementedError


def forward_log_likelihood(observations, model):
    """Return log P(observations | model) using the Forward algorithm."""
    raise NotImplementedError


def viterbi_decode(observations, model):
    """Return the best-path log probability and deterministic state path."""
    raise NotImplementedError


def forward_backward(observations, model):
    """Return posterior state probabilities at each observation position."""
    raise NotImplementedError
'''

_DECODING_CHECKS = """
model = {
    "states": ("H", "L"),
    "initial": {"H": 0.5, "L": 0.5},
    "transition": {
        "H": {"H": 0.8, "L": 0.2},
        "L": {"H": 0.2, "L": 0.8},
    },
    "emission": {
        "H": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1},
        "L": {"A": 0.4, "C": 0.1, "G": 0.1, "T": 0.4},
    },
}
score, path = viterbi_decode("GGGCAATT", model)
print(round(score, 6), "".join(path))
posteriors = forward_backward("ACGT", model)
rounded = [{state: round(probability, 3) for state, probability in row.items()} for row in posteriors]
print(rounded)
"""


DM847_LAB_04 = ComputationalLab(
    lab_id="dm847.lab04.hidden-markov-models",
    course_code="DM847",
    version="1.0.0",
    title=_text(
        "Laboratorio 4: modelos ocultos de Markov",
        "Laboratory 4: hidden Markov models",
        "Laboratorium 4: skjulte Markov-modeller",
    ),
    research_question=_text(
        "¿Cómo cambian nuestras conclusiones sobre estados biológicos no observados cuando calculamos probabilidad total, trayectoria más probable y posterior por posición?",
        "How do conclusions about unobserved biological states change when we compute total probability, the most probable path, and position-wise posterior probabilities?",
        "Hvordan ændres konklusioner om uobserverede biologiske tilstande, når vi beregner samlet sandsynlighed, den mest sandsynlige sti og positionsvise posteriorer?",
    ),
    disclaimer=_text(
        "Preparación interna basada en los resultados de aprendizaje de DM847. No reproduce una hoja oficial de laboratorio de SDU.",
        "Internal preparation based on DM847 learning outcomes. It does not reproduce an official SDU laboratory sheet.",
        "Intern forberedelse baseret på læringsmålene i DM847. Den gengiver ikke et officielt SDU-laboratorieark.",
    ),
    data_provenance=_text(
        "Las secuencias, estados y probabilidades son sintéticos y se diseñaron para enseñar inferencia en HMM. No representan anotaciones genómicas, pacientes ni probabilidades clínicas calibradas.",
        "The sequences, states, and probabilities are synthetic and were designed to teach HMM inference. They do not represent genomic annotations, patients, or calibrated clinical probabilities.",
        "Sekvenser, tilstande og sandsynligheder er syntetiske og designet til at undervise i HMM-inferens. De repræsenterer ikke genomiske annotationer, patienter eller kalibrerede kliniske sandsynligheder.",
    ),
    objectives=(
        (
            "dm847.lab04.contract",
            _text(
                "Definir estados, observaciones, probabilidades iniciales, transiciones y emisiones.",
                "Define states, observations, initial probabilities, transitions, and emissions.",
                "Definere tilstande, observationer, startsandsynligheder, overgange og emissioner.",
            ),
        ),
        (
            "dm847.lab04.forward",
            _text(
                "Implementar Forward en espacio logarítmico y calcular la probabilidad total de una secuencia.",
                "Implement Forward in log space and calculate the total probability of a sequence.",
                "Implementere Forward i log-rum og beregne en sekvens' samlede sandsynlighed.",
            ),
        ),
        (
            "dm847.lab04.viterbi",
            _text(
                "Implementar Viterbi con desempate determinista y reconstrucción de trayectoria.",
                "Implement Viterbi with deterministic tie-breaking and path reconstruction.",
                "Implementere Viterbi med deterministisk tie-breaking og rekonstruktion af sti.",
            ),
        ),
        (
            "dm847.lab04.posterior",
            _text(
                "Aplicar Forward–Backward para obtener probabilidades posteriores por posición.",
                "Apply Forward–Backward to obtain position-wise posterior probabilities.",
                "Anvende Forward–Backward til at opnå positionsvise posterior-sandsynligheder.",
            ),
        ),
        (
            "dm847.lab04.numerics",
            _text(
                "Explicar underflow, log-sum-exp y comprobaciones de normalización.",
                "Explain underflow, log-sum-exp, and normalization checks.",
                "Forklare underflow, log-sum-exp og normaliseringskontroller.",
            ),
        ),
        (
            "dm847.lab04.interpretation",
            _text(
                "Distinguir probabilidad de observaciones, mejor trayectoria y posterior marginal sin sobreinterpretar estados latentes.",
                "Distinguish observation likelihood, best path, and marginal posterior without overinterpreting latent states.",
                "Skelne observationssandsynlighed, bedste sti og marginal posterior uden at overfortolke latente tilstande.",
            ),
        ),
    ),
    prerequisites=(
        _text(
            "Probabilidad condicional, regla del producto y suma sobre alternativas.",
            "Conditional probability, the product rule, and summation over alternatives.",
            "Betinget sandsynlighed, produktreglen og summering over alternativer.",
        ),
        _text(
            "Programación dinámica, matrices y traceback del Laboratorio 2.",
            "Dynamic programming, matrices, and traceback from Laboratory 2.",
            "Dynamisk programmering, matricer og traceback fra Laboratorium 2.",
        ),
        _text(
            "Logaritmos y representación de probabilidades pequeñas.",
            "Logarithms and representation of small probabilities.",
            "Logaritmer og repræsentation af små sandsynligheder.",
        ),
    ),
    tasks=(
        LabTask(
            task_id="dm847.lab04.prepare.model-contract",
            stage=LabStage.PREPARE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Contrato del HMM", "HMM contract", "HMM-kontrakt"),
            instructions=_text(
                "Define qué representan H y L, el alfabeto observado, la distribución inicial, las filas de transición y emisión, la política para secuencia vacía y el orden usado para desempatar estados.",
                "Define what H and L represent, the observation alphabet, initial distribution, transition and emission rows, empty-sequence policy, and state order used for ties.",
                "Definér hvad H og L repræsenterer, observationsalfabetet, startfordelingen, overgangs- og emissionsrækker, politikken for tom sekvens og tilstandsordenen ved ties.",
            ),
            mentor_notes=_text(
                "Pregunta primero qué es observado y qué permanece latente. Después exige que cada distribución sume uno y que el estudiante explique la independencia condicional asumida.",
                "First ask what is observed and what remains latent. Then require every distribution to sum to one and the learner to explain the conditional-independence assumption.",
                "Spørg først hvad der observeres, og hvad der forbliver latent. Kræv derefter at hver fordeling summerer til én, og at den studerende forklarer antagelsen om betinget uafhængighed.",
            ),
            objective_ids=("dm847.lab04.contract", "dm847.lab04.interpretation"),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm847.lab04.investigate.manual-forward",
            stage=LabStage.INVESTIGATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Forward y Viterbi a mano",
                "Manual Forward and Viterbi",
                "Manuel Forward og Viterbi",
            ),
            instructions=_text(
                "Para una secuencia corta, calcula las primeras dos columnas de Forward y Viterbi. Explica por qué Forward suma trayectorias mientras Viterbi conserva sólo el máximo y predice cuándo sus resultados pueden divergir.",
                "For a short sequence, calculate the first two Forward and Viterbi columns. Explain why Forward sums paths while Viterbi retains only the maximum, and predict when their conclusions can diverge.",
                "Beregn de første to Forward- og Viterbi-kolonner for en kort sekvens. Forklar hvorfor Forward summerer stier, mens Viterbi kun bevarer maksimum, og forudsig hvornår konklusionerne kan afvige.",
            ),
            mentor_notes=_text(
                "No proporciones la tabla completa. Pide primero el significado de cada celda y localiza la primera multiplicación, suma o máximo incorrecto.",
                "Do not provide the complete table. First request the meaning of each cell and locate the first incorrect multiplication, sum, or maximum.",
                "Giv ikke hele tabellen. Bed først om betydningen af hver celle og lokalisér den første forkerte multiplikation, sum eller maksimum.",
            ),
            objective_ids=("dm847.lab04.forward", "dm847.lab04.viterbi"),
            estimated_minutes=20,
        ),
        LabTask(
            task_id="dm847.lab04.implement.forward-log",
            stage=LabStage.IMPLEMENT,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Forward estable en logaritmos",
                "Stable log-space Forward",
                "Stabil Forward i log-rum",
            ),
            instructions=_text(
                "Implementa validación del modelo, logsumexp y forward_log_likelihood. La secuencia vacía debe tener log-probabilidad 0. Rechaza modelos no normalizados, probabilidades no positivas y símbolos no emitibles.",
                "Implement model validation, logsumexp, and forward_log_likelihood. The empty sequence must have log probability 0. Reject unnormalized models, non-positive probabilities, and non-emittable symbols.",
                "Implementér modelvalidering, logsumexp og forward_log_likelihood. Den tomme sekvens skal have log-sandsynlighed 0. Afvis ikke-normaliserede modeller, ikke-positive sandsynligheder og symboler der ikke kan emitteres.",
            ),
            mentor_notes=_text(
                "Pregunta por el estado de la recurrencia, el caso base y por qué log(a+b) no es log(a)+log(b). Ofrece la identidad log-sum-exp sólo después de una explicación conceptual.",
                "Ask about recurrence state, the base case, and why log(a+b) is not log(a)+log(b). Offer the log-sum-exp identity only after a conceptual explanation.",
                "Spørg til rekurrensens tilstand, basistilfældet og hvorfor log(a+b) ikke er log(a)+log(b). Giv først log-sum-exp-identiteten efter en konceptuel forklaring.",
            ),
            objective_ids=(
                "dm847.lab04.contract",
                "dm847.lab04.forward",
                "dm847.lab04.numerics",
            ),
            estimated_minutes=35,
            starter_response=_FORWARD_STARTER,
            verification_source=_FORWARD_CHECKS,
            expected_output="-5.977167\n-10.23519",
        ),
        LabTask(
            task_id="dm847.lab04.check.viterbi-posterior",
            stage=LabStage.CHECK,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Viterbi y Forward–Backward",
                "Viterbi and Forward–Backward",
                "Viterbi og Forward–Backward",
            ),
            instructions=_text(
                "Implementa Viterbi con prioridad por el orden declarado de estados y Forward–Backward en espacio logarítmico. Devuelve una trayectoria completa y una distribución posterior normalizada en cada posición.",
                "Implement Viterbi with priority given by declared state order and Forward–Backward in log space. Return a complete path and a normalized posterior distribution at every position.",
                "Implementér Viterbi med prioritet efter den deklarerede tilstandsorden og Forward–Backward i log-rum. Returnér en komplet sti og en normaliseret posterior-fordeling ved hver position.",
            ),
            mentor_notes=_text(
                "Ante un fallo, exige comprobar longitud de trayectoria, recálculo de la probabilidad del camino, suma posterior igual a uno y uso de evidencia futura en beta. No reveles las pruebas internas.",
                "On failure, require checks for path length, recomputed path probability, posterior sums equal to one, and use of future evidence in beta. Do not reveal internal tests.",
                "Ved fejl skal du kræve kontrol af stilængde, genberegnet stisandsynlighed, posterior-summer lig én og brug af fremtidig evidens i beta. Afslør ikke interne tests.",
            ),
            objective_ids=(
                "dm847.lab04.viterbi",
                "dm847.lab04.posterior",
                "dm847.lab04.numerics",
            ),
            estimated_minutes=45,
            starter_response=_DECODING_STARTER,
            verification_source=_DECODING_CHECKS,
            expected_output=(
                "-10.971772 HHHHLLLL\n"
                "[{'H': 0.382, 'L': 0.618}, {'H': 0.732, 'L': 0.268}, "
                "{'H': 0.732, 'L': 0.268}, {'H': 0.382, 'L': 0.618}]"
            ),
        ),
        LabTask(
            task_id="dm847.lab04.interpret.path-versus-posterior",
            stage=LabStage.INTERPRET,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Trayectoria global y posterior marginal",
                "Global path and marginal posterior",
                "Global sti og marginal posterior",
            ),
            instructions=_text(
                "Compara la trayectoria Viterbi y los posteriores de ACGT y GGGCAATT. Identifica posiciones inciertas y explica por qué el estado marginal más probable en cada posición no tiene que formar la trayectoria global más probable.",
                "Compare the Viterbi path and posteriors for ACGT and GGGCAATT. Identify uncertain positions and explain why the most probable marginal state at each position need not form the globally most probable path.",
                "Sammenlign Viterbi-stien og posteriorerne for ACGT og GGGCAATT. Identificér usikre positioner og forklar hvorfor den mest sandsynlige marginale tilstand ved hver position ikke behøver at danne den globalt mest sandsynlige sti.",
            ),
            mentor_notes=_text(
                "Exige separar P(x), P(path,x), P(path|x) y P(state_t|x). Pregunta qué información futura modifica el posterior y qué incertidumbre pierde Viterbi.",
                "Require separation of P(x), P(path,x), P(path|x), and P(state_t|x). Ask which future evidence changes the posterior and which uncertainty Viterbi discards.",
                "Kræv adskillelse af P(x), P(path,x), P(path|x) og P(state_t|x). Spørg hvilken fremtidig evidens der ændrer posterioren, og hvilken usikkerhed Viterbi kasserer.",
            ),
            objective_ids=("dm847.lab04.posterior", "dm847.lab04.interpretation"),
            estimated_minutes=25,
        ),
        LabTask(
            task_id="dm847.lab04.defend.model-assumptions",
            stage=LabStage.DEFEND,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Defensa del modelo y la complejidad",
                "Model and complexity defence",
                "Forsvar af model og kompleksitet",
            ),
            instructions=_text(
                "Defiende la complejidad temporal y espacial de Forward, Viterbi y Forward–Backward usando T observaciones y K estados. Evalúa Markov de primer orden, emisiones condicionalmente independientes, parámetros conocidos y estabilidad numérica.",
                "Defend the time and space complexity of Forward, Viterbi, and Forward–Backward using T observations and K states. Evaluate first-order Markov structure, conditionally independent emissions, known parameters, and numerical stability.",
                "Forsvar tids- og rumkompleksiteten for Forward, Viterbi og Forward–Backward med T observationer og K tilstande. Vurdér førsteordens Markov-struktur, betinget uafhængige emissioner, kendte parametre og numerisk stabilitet.",
            ),
            mentor_notes=_text(
                "Solicita primero T y K, después separa coste de puntuación, traceback y posterior. Exige una consecuencia concreta de cada supuesto sobre la interpretación biomédica.",
                "First request T and K, then separate scoring, traceback, and posterior costs. Require one concrete biomedical interpretation consequence for every assumption.",
                "Bed først om T og K, og adskil derefter omkostninger til scoring, traceback og posterior. Kræv én konkret biomedicinsk fortolkningskonsekvens for hver antagelse.",
            ),
            objective_ids=(
                "dm847.lab04.forward",
                "dm847.lab04.viterbi",
                "dm847.lab04.posterior",
                "dm847.lab04.interpretation",
            ),
            estimated_minutes=25,
        ),
        LabTask(
            task_id="dm847.lab04.consolidate.hmm-audit",
            stage=LabStage.CONSOLIDATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Auditoría del HMM", "HMM audit", "HMM-audit"),
            instructions=_text(
                "Registra el error más importante, su síntoma, causa, corrección y prueba de regresión. Selecciona una extensión prioritaria: escalado explícito, Baum–Welch, más estados, duraciones o validación con etiquetas externas.",
                "Record the most important error, its symptom, cause, correction, and regression test. Select one priority extension: explicit scaling, Baum–Welch, more states, durations, or validation against external labels.",
                "Registrér den vigtigste fejl, dens symptom, årsag, rettelse og regressionstest. Vælg én prioriteret udvidelse: eksplicit skalering, Baum–Welch, flere tilstande, varigheder eller validering mod eksterne labels.",
            ),
            mentor_notes=_text(
                "No aceptes una reflexión genérica. Exige evidencia del error, un test reproducible y una razón científica para priorizar la extensión.",
                "Do not accept a generic reflection. Require evidence of the error, a reproducible test, and a scientific reason for prioritizing the extension.",
                "Acceptér ikke en generisk refleksion. Kræv evidens for fejlen, en reproducerbar test og en videnskabelig grund til at prioritere udvidelsen.",
            ),
            objective_ids=(
                "dm847.lab04.contract",
                "dm847.lab04.numerics",
                "dm847.lab04.interpretation",
            ),
            estimated_minutes=20,
        ),
    ),
    estimated_minutes=185,
)


__all__ = ["DM847_LAB_04"]
