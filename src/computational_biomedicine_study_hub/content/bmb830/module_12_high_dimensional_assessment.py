"""Assessment data for BMB830 module 12."""

from __future__ import annotations

from .module_12_high_dimensional_text import tr

MCQS = (
    (
        "001",
        tr(
            "¿Qué debe preceder al análisis?",
            "What should precede analysis?",
            "Hvad bør gå forud for analysen?",
        ),
        (
            (
                "a",
                tr("Contrato y procedencia", "Contract and provenance", "Kontrakt og proveniens"),
            ),
            (
                "b",
                tr(
                    "Elegir la figura más separada",
                    "Choose the most separated figure",
                    "Vælg figuren med størst adskillelse",
                ),
            ),
        ),
        "a",
        tr(
            "La procedencia define qué representan los datos.",
            "Provenance defines what data represent.",
            "Proveniens definerer hvad data repræsenterer.",
        ),
    ),
    (
        "002",
        tr(
            "¿Qué significa p mayor que n?",
            "What does p greater than n mean?",
            "Hvad betyder p større end n?",
        ),
        (
            (
                "a",
                tr(
                    "Más variables que pacientes",
                    "More variables than patients",
                    "Flere variable end patienter",
                ),
            ),
            (
                "b",
                tr(
                    "Más pacientes independientes",
                    "More independent patients",
                    "Flere uafhængige patienter",
                ),
            ),
        ),
        "a",
        tr(
            "Las características no aumentan unidades independientes.",
            "Features do not increase independent units.",
            "Features øger ikke uafhængige enheder.",
        ),
    ),
    (
        "003",
        tr(
            "¿Qué filtro es independiente de enfermedad?",
            "Which filter is independent of disease?",
            "Hvilket filter er uafhængigt af sygdom?",
        ),
        (
            (
                "a",
                tr(
                    "Ausencia y varianza cero",
                    "Missingness and zero variance",
                    "Manglende værdier og nulvarians",
                ),
            ),
            (
                "b",
                tr(
                    "Mayor diferencia entre grupos",
                    "Largest group difference",
                    "Største gruppeforskel",
                ),
            ),
        ),
        "a",
        tr(
            "Es control de calidad no supervisado.",
            "It is unsupervised quality control.",
            "Det er usuperviseret kvalitetskontrol.",
        ),
    ),
    (
        "004",
        tr(
            "¿Dónde se estiman medianas predictivas?",
            "Where are predictive medians estimated?",
            "Hvor estimeres prædiktive medianer?",
        ),
        (
            ("a", tr("Solo entrenamiento", "Training only", "Kun træning")),
            ("b", tr("Todos los pacientes", "All patients", "Alle patienter")),
        ),
        "a",
        tr(
            "La validación no puede influir.",
            "Validation cannot influence them.",
            "Validering må ikke påvirke dem.",
        ),
    ),
    (
        "005",
        tr(
            "PC1 se asocia con lote. ¿Qué priorizar?",
            "PC1 is associated with batch. What should be prioritised?",
            "PC1 er associeret med batch. Hvad prioriteres?",
        ),
        (
            ("a", tr("Investigar lote", "Investigate batch", "Undersøg batch")),
            ("b", tr("Declarar subtipo", "Declare a subtype", "Erklær en undertype")),
        ),
        "a",
        tr(
            "La variación técnica puede dominar.",
            "Technical variation may dominate.",
            "Teknisk variation kan dominere.",
        ),
    ),
    (
        "006",
        tr(
            "¿Qué requiere un cribado de 240 proteínas?",
            "What does screening 240 proteins require?",
            "Hvad kræver screening af 240 proteiner?",
        ),
        (
            (
                "a",
                tr(
                    "Multiplicidad y validación",
                    "Multiplicity and validation",
                    "Multiplicitet og validering",
                ),
            ),
            ("b", tr("Solo ranking", "Ranking only", "Kun rangering")),
        ),
        "a",
        tr(
            "Muchas comparaciones generan hallazgos casuales.",
            "Many comparisons generate chance findings.",
            "Mange sammenligninger skaber tilfældige fund.",
        ),
    ),
    (
        "007",
        tr(
            "¿Qué afirma correctamente el caso?",
            "What does the case correctly claim?",
            "Hvad hævder casen korrekt?",
        ),
        (
            (
                "a",
                tr(
                    "Practica un flujo sintético",
                    "It practises a synthetic workflow",
                    "Den træner et syntetisk workflow",
                ),
            ),
            (
                "b",
                tr("Valida biomarcadores", "It validates biomarkers", "Den validerer biomarkører"),
            ),
        ),
        "a",
        tr(
            "No contiene evidencia clínica real.",
            "It contains no real clinical evidence.",
            "Den indeholder ingen reel klinisk evidens.",
        ),
    ),
    (
        "008",
        tr("¿Qué puede hacer Ollama?", "What may Ollama do?", "Hvad må Ollama gøre?"),
        (
            ("a", tr("Revisar claridad", "Review clarity", "Gennemgå klarhed")),
            ("b", tr("Certificar números", "Certify numbers", "Certificere tal")),
        ),
        "a",
        tr(
            "La evaluación numérica sigue siendo determinista.",
            "Numerical assessment remains deterministic.",
            "Numerisk vurdering forbliver deterministisk.",
        ),
    ),
)

TRUE_FALSE = (
    (
        "009",
        tr(
            "240 proteínas equivalen a 240 pacientes.",
            "240 proteins equal 240 patients.",
            "240 proteiner svarer til 240 patienter.",
        ),
        False,
        tr(
            "Variables y unidades son diferentes.",
            "Variables and units differ.",
            "Variable og enheder er forskellige.",
        ),
    ),
    (
        "010",
        tr(
            "La ausencia debe resumirse por paciente y proteína.",
            "Missingness should be summarised by patient and protein.",
            "Manglende værdier bør opsummeres pr. patient og protein.",
        ),
        True,
        tr("Ambas direcciones importan.", "Both directions matter.", "Begge retninger er vigtige."),
    ),
    (
        "011",
        tr("PCA puede revelar lote.", "PCA can reveal batch.", "PCA kan afsløre batch."),
        True,
        tr(
            "Ordena variación sin conocer su causa.",
            "It orders variation without knowing its cause.",
            "Den ordner variation uden at kende dens årsag.",
        ),
    ),
    (
        "012",
        tr(
            "Imputar antes de dividir siempre es seguro.",
            "Imputing before splitting is always safe.",
            "Imputering før opdeling er altid sikker.",
        ),
        False,
        tr("Puede producir fuga.", "It may cause leakage.", "Det kan skabe lækage."),
    ),
    (
        "013",
        tr(
            "Una lista top demuestra biomarcadores.",
            "A top list proves biomarkers.",
            "En topliste beviser biomarkører.",
        ),
        False,
        tr(
            "Requiere validación independiente.",
            "Independent validation is required.",
            "Uafhængig validering kræves.",
        ),
    ),
    (
        "014",
        tr(
            "Los datos sintéticos permiten probar la tubería.",
            "Synthetic data can test the pipeline.",
            "Syntetiske data kan teste pipelinen.",
        ),
        True,
        tr(
            "No sustituyen evidencia externa.",
            "They do not replace external evidence.",
            "De erstatter ikke ekstern evidens.",
        ),
    ),
    (
        "015",
        tr(
            "Ollama puede cambiar dominio por estilo.",
            "Ollama may change mastery based on style.",
            "Ollama må ændre mestring ud fra stil.",
        ),
        False,
        tr("Solo apoya escritura.", "It only supports writing.", "Den understøtter kun skrivning."),
    ),
    (
        "016",
        tr(
            "El reporte debe separar hallazgos y limitaciones.",
            "The report should separate findings and limitations.",
            "Rapporten bør adskille fund og begrænsninger.",
        ),
        True,
        tr(
            "La transparencia limita sobreinterpretación.",
            "Transparency limits overinterpretation.",
            "Transparens begrænser overfortolkning.",
        ),
    ),
)

TUTOR = (
    tr(
        "El caso integra procedencia, QC, PCA, lote, cribado y reporte con una frontera sintética explícita.",
        "The case integrates provenance, QC, PCA, batch, screening, and reporting with an explicit synthetic boundary.",
        "Casen integrerer proveniens, QC, PCA, batch, screening og rapportering med en eksplicit syntetisk grænse.",
    ),
    (
        tr(
            "La matriz contiene 48 pacientes y 240 proteínas.",
            "The matrix contains 48 patients and 240 proteins.",
            "Matricen indeholder 48 patienter og 240 proteiner.",
        ),
        tr(
            "El ranking usa solo entrenamiento.",
            "Ranking uses training only.",
            "Rangering bruger kun træning.",
        ),
    ),
    (
        tr("PCA confirma enfermedad.", "PCA confirms disease.", "PCA bekræfter sygdom."),
        tr(
            "Top 10 equivale a panel clínico.",
            "Top 10 equals a clinical panel.",
            "Top 10 svarer til et klinisk panel.",
        ),
    ),
    (
        tr(
            "¿Qué representa cada fila?",
            "What does each row represent?",
            "Hvad repræsenterer hver række?",
        ),
        tr(
            "¿Qué se aprendió solo con entrenamiento?",
            "What was learned from training only?",
            "Hvad blev kun lært fra træning?",
        ),
    ),
    (
        tr(
            "Justifica QC y preprocesamiento.",
            "Justifies QC and preprocessing.",
            "Begrunder QC og forbehandling.",
        ),
        tr(
            "Distingue exploración y validación.",
            "Distinguishes exploration and validation.",
            "Skelner mellem eksploration og validering.",
        ),
    ),
    (
        tr(
            "No presentar datos sintéticos como evidencia clínica.",
            "Do not present synthetic data as clinical evidence.",
            "Præsentér ikke syntetiske data som klinisk evidens.",
        ),
        tr(
            "No usar Ollama para certificar números.",
            "Do not use Ollama to certify numbers.",
            "Brug ikke Ollama til at certificere tal.",
        ),
    ),
    ("bmb830.m12.concepts", "bmb830.m12.examples", "bmb830.m12.practice", "bmb830.m12.assessment"),
)
