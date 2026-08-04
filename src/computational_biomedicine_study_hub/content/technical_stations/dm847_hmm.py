"""Technical reasoning stations for DM847 hidden Markov models."""

from __future__ import annotations

from ...learning.technical_stations import TechnicalStation, TechnicalStationKind
from ._shared import criterion, localized

LAB_ID = "dm847.lab04.hidden-markov-models"

DM847_HMM_STATIONS = (
    TechnicalStation(
        station_id="dm847.lab04.station.read-logsumexp",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.CODE_READING,
        title=localized(
            "Leer log-sum-exp",
            "Read log-sum-exp",
            "Læs log-sum-exp",
        ),
        artifact_title=localized("Código", "Code", "Kode"),
        artifact="""def logsumexp(values: list[float]) -> float:
    maximum = max(values)
    return maximum + log(sum(exp(value - maximum) for value in values))""",
        prompt=localized(
            "Deriva por qué la expresión es equivalente a log(sum(exp(values))) y explica "
            "cómo restar maximum mejora la estabilidad numérica sin cambiar el resultado "
            "matemático.",
            "Derive why the expression equals log(sum(exp(values))) and explain how "
            "subtracting maximum improves numerical stability without changing the "
            "mathematical result.",
            "Udled hvorfor udtrykket er lig log(sum(exp(values))) og forklar hvordan "
            "subtraktion af maximum forbedrer numerisk stabilitet uden at ændre det "
            "matematiske resultat.",
        ),
        criteria=(
            criterion(
                "identity",
                "Factoriza exp(maximum) dentro de la suma.",
                "Factor exp(maximum) out of the sum.",
                "Faktoriser exp(maximum) ud af summen.",
            ),
            criterion(
                "stability",
                "Explica que los exponentes desplazados son <= 0 y evitan overflow.",
                "Explain that shifted exponents are <= 0 and avoid overflow.",
                "Forklar at forskudte eksponenter er <= 0 og undgår overflow.",
            ),
            criterion(
                "edge",
                "Menciona el contrato necesario para lista vacía o valores -inf.",
                "Mention the required contract for an empty list or -inf values.",
                "Nævn den nødvendige kontrakt for en tom liste eller -inf-værdier.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 numerical stability in HMMs"),
    ),
    TechnicalStation(
        station_id="dm847.lab04.station.trace-forward-viterbi",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=localized(
            "Separar Forward y Viterbi en una columna",
            "Separate Forward and Viterbi in one column",
            "Adskil Forward og Viterbi i én kolonne",
        ),
        artifact_title=localized(
            "Valores previos",
            "Previous values",
            "Tidligere værdier",
        ),
        artifact="""Previous log scores for states H and L: [-1.0, -1.4]
Transitions into H: log(0.8), log(0.2)
Emission of G from H: log(0.4)

Compute:
1. Forward score for H at the next position
2. Viterbi score for H at the next position""",
        prompt=localized(
            "Escribe las dos expresiones, identifica dónde se usa suma logarítmica y dónde "
            "máximo, y explica qué información descarta Viterbi.",
            "Write both expressions, identify where log-sum is used and where max is used, "
            "and explain which information Viterbi discards.",
            "Skriv begge udtryk, identificér hvor log-sum bruges og hvor max bruges, og "
            "forklar hvilken information Viterbi kasserer.",
        ),
        criteria=(
            criterion(
                "forward",
                "Forward combina ambas rutas mediante logsumexp antes de la emisión.",
                "Forward combines both paths with logsumexp before the emission.",
                "Forward kombinerer begge stier med logsumexp før emissionen.",
            ),
            criterion(
                "viterbi",
                "Viterbi conserva el máximo y registra su predecesor.",
                "Viterbi retains the maximum and records its predecessor.",
                "Viterbi bevarer maksimum og registrerer forgængeren.",
            ),
            criterion(
                "information",
                "Explica que Viterbi descarta masa de probabilidad de rutas no máximas.",
                "Explain that Viterbi discards probability mass from non-maximal paths.",
                "Forklar at Viterbi kasserer sandsynlighedsmasse fra ikke-maksimale stier.",
            ),
        ),
        estimated_minutes=15,
        source_basis=(LAB_ID, "DM847 Forward versus Viterbi"),
    ),
    TechnicalStation(
        station_id="dm847.lab04.station.debug-backward-init",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.DEBUGGING,
        title=localized(
            "Depurar la inicialización Backward",
            "Debug Backward initialization",
            "Fejlfind Backward-initialisering",
        ),
        artifact_title=localized(
            "Código defectuoso",
            "Defective code",
            "Defekt kode",
        ),
        artifact="""beta = [[float("-inf")] * K for _ in range(T)]
for state in range(K):
    beta[T - 1][state] = log(initial[state])

# Posterior rows no longer sum to 1 after combining alpha and beta.""",
        prompt=localized(
            "Identifica el error conceptual, corrige la condición terminal y explica por qué "
            "usar initial dos veces distorsiona los posteriores.",
            "Identify the conceptual error, correct the terminal condition, and explain why "
            "using initial twice distorts the posteriors.",
            "Identificér den konceptuelle fejl, ret terminalbetingelsen og forklar hvorfor "
            "brug af initial to gange forvrider posteriorerne.",
        ),
        criteria=(
            criterion(
                "terminal",
                "Establece beta[T-1][state] = 0.0 en espacio log.",
                "Set beta[T-1][state] = 0.0 in log space.",
                "Sæt beta[T-1][state] = 0.0 i log-rum.",
            ),
            criterion(
                "meaning",
                "Explica que no queda evidencia futura tras la última observación.",
                "Explain that no future evidence remains after the final observation.",
                "Forklar at der ikke er fremtidig evidens efter den sidste observation.",
            ),
            criterion(
                "effect",
                "Relaciona el doble uso de initial con normalización posterior incorrecta.",
                "Relate double use of initial to incorrect posterior normalization.",
                "Knyt dobbelt brug af initial til forkert posterior-normalisering.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 Forward-Backward invariants"),
    ),
    TechnicalStation(
        station_id="dm847.lab04.station.interpret-path-posterior",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.OUTPUT_INTERPRETATION,
        title=localized(
            "Interpretar trayectoria y posteriores",
            "Interpret path and posteriors",
            "Fortolk sti og posteriorer",
        ),
        artifact_title=localized("Salida", "Output", "Output"),
        artifact="""observations = ACGT
viterbi_path = HHHH
posterior P(H | full sequence) = [0.382, 0.732, 0.732, 0.382]""",
        prompt=localized(
            "Explica por qué la trayectoria Viterbi puede ser HHHH aunque L tenga posterior "
            "marginal mayor en posiciones 1 y 4. Distingue trayectoria conjunta óptima, estado "
            "marginal y evidencia biológica.",
            "Explain why the Viterbi path can be HHHH even though L has the larger marginal "
            "posterior at positions 1 and 4. Distinguish optimal joint path, marginal state, "
            "and biological evidence.",
            "Forklar hvorfor Viterbi-stien kan være HHHH selv om L har større marginal "
            "posterior ved position 1 og 4. Skeln optimal fælles sti, marginal tilstand og "
            "biologisk evidens.",
        ),
        criteria=(
            criterion(
                "joint",
                "Define Viterbi como una trayectoria conjunta global.",
                "Define Viterbi as one global joint path.",
                "Definér Viterbi som én global fælles sti.",
            ),
            criterion(
                "marginal",
                "Define cada posterior como suma sobre trayectorias compatibles en una posición.",
                "Define each posterior as a sum over compatible paths at one position.",
                "Definér hver posterior som en sum over kompatible stier ved én position.",
            ),
            criterion(
                "boundary",
                "Aclara que H/L son estados sintéticos y no anotaciones biológicas validadas.",
                "Clarify that H/L are synthetic states, not validated biological annotations.",
                "Præcisér at H/L er syntetiske tilstande, ikke validerede biologiske annotationer.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(
            LAB_ID,
            "DM847 posterior uncertainty interpretation",
        ),
    ),
)

__all__ = ["DM847_HMM_STATIONS"]
