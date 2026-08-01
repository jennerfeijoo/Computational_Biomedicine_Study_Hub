"""Localized text for BMB830 module 12."""

from __future__ import annotations

T = tuple[str, str, str]


def tr(es: str, en: str, da: str) -> T:
    return es, en, da


TITLE = tr(
    "Caso individual de proteómica de alta dimensión",
    "Individual high-dimensional proteomics case",
    "Individuel case med højdimensional proteomik",
)

SUMMARY = tr(
    "Integra procedencia, control de calidad, filtrado, imputación, log2, escalado, PCA, lote, cribado y reporte reproducible en una matriz sintética con p mayor que n.",
    "Integrate provenance, quality control, filtering, imputation, log2, scaling, PCA, batch, screening, and reproducible reporting in a synthetic matrix with p greater than n.",
    "Integrér proveniens, kvalitetskontrol, filtrering, imputering, log2, skalering, PCA, batch, screening og reproducerbar rapportering i en syntetisk matrix med p større end n.",
)

OBJECTIVES = (
    (
        "m12.o1",
        tr(
            "Auditar procedencia, diccionario de datos, pacientes, dimensiones y metadatos.",
            "Audit provenance, the data dictionary, patients, dimensions, and metadata.",
            "Revidere proveniens, dataordbog, patienter, dimensioner og metadata.",
        ),
    ),
    (
        "m12.o2",
        tr(
            "Construir control de calidad, filtrado e imputación reproducibles cuando p es mayor que n.",
            "Build reproducible quality control, filtering, and imputation when p exceeds n.",
            "Opbygge reproducerbar kvalitetskontrol, filtrering og imputering når p overstiger n.",
        ),
    ),
    (
        "m12.o3",
        tr(
            "Evaluar PCA, lote y cribado sin fuga de información.",
            "Assess PCA, batch, and screening without information leakage.",
            "Vurdere PCA, batch og screening uden informationslækage.",
        ),
    ),
    (
        "m12.o4",
        tr(
            "Redactar un informe individual sin presentar datos sintéticos como evidencia clínica.",
            "Write an individual report without presenting synthetic data as clinical evidence.",
            "Skrive en individuel rapport uden at fremstille syntetiske data som klinisk evidens.",
        ),
    ),
)

CONCEPTS = (
    (
        "provenance",
        tr(
            "Procedencia y contrato de datos",
            "Provenance and data contract",
            "Proveniens og datakontrakt",
        ),
        tr(
            "Registrar origen, versión, fecha, unidad de observación, identificadores, unidades y códigos de ausencia precede al análisis. Esta matriz es sintética y sirve para practicar; no estima prevalencia ni valida biomarcadores.",
            "Record origin, version, date, observational unit, identifiers, units, and missing-value codes before analysis. This matrix is synthetic practice material; it estimates no prevalence and validates no biomarkers.",
            "Registrér oprindelse, version, dato, observationsenhed, identifikatorer, enheder og koder for manglende værdier før analysen. Matricen er syntetisk øvelsesmateriale og estimerer ingen prævalens eller validerer biomarkører.",
        ),
        (
            tr(
                "La clave paciente debe ser única y coincidir con las filas.",
                "Patient keys must be unique and match rows.",
                "Patientnøgler skal være entydige og matche rækker.",
            ),
            tr(
                "El diccionario de datos fija significado y unidades.",
                "The data dictionary fixes meaning and units.",
                "Dataordbogen fastlægger betydning og enheder.",
            ),
        ),
    ),
    (
        "qc",
        tr(
            "Control de calidad con p mayor que n",
            "Quality control with p greater than n",
            "Kvalitetskontrol med p større end n",
        ),
        tr(
            "Más proteínas que pacientes aumentan oportunidades de asociaciones casuales, no el número de unidades independientes. Verifica dimensiones, duplicados, correspondencia, ausencia por muestra y característica, varianza cero, rangos y memoria aproximada antes de mirar grupos.",
            "More proteins than patients increase opportunities for chance associations, not independent units. Check dimensions, duplicates, correspondence, sample and feature missingness, zero variance, ranges, and approximate memory before viewing groups.",
            "Flere proteiner end patienter øger mulighederne for tilfældige associationer, ikke antallet af uafhængige enheder. Kontrollér dimensioner, dubletter, overensstemmelse, manglende værdier pr. prøve og feature, nulvarians, intervaller og omtrentligt hukommelsesforbrug før grupper undersøges.",
        ),
        (
            tr(
                "Ausencia por muestra y por característica responden preguntas distintas.",
                "Sample and feature missingness answer different questions.",
                "Manglende værdier pr. prøve og feature besvarer forskellige spørgsmål.",
            ),
            tr(
                "Los umbrales se documentan antes de optimizar figuras.",
                "Thresholds are documented before optimising figures.",
                "Tærskler dokumenteres før figurer optimeres.",
            ),
        ),
    ),
    (
        "preprocessing",
        tr(
            "Filtrado, imputación y fuga",
            "Filtering, imputation, and leakage",
            "Filtrering, imputering og lækage",
        ),
        tr(
            "Filtra características no analizables mediante reglas previas; imputa bajo supuestos; usa log2 para intensidades positivas cuando esté justificado; y escala según la pregunta. En predicción, filtros, medianas, medias, desviaciones, PCA y cribado se aprenden solo con entrenamiento.",
            "Filter non-analysable features using prior rules; impute under assumptions; use log2 for positive intensities when justified; and scale according to the question. In prediction, filters, medians, means, standard deviations, PCA, and screening are learned from training only.",
            "Filtrér ikke-analyserbare features med forudgående regler; imputér under antagelser; brug log2 til positive intensiteter når det er begrundet; og skalér efter spørgsmålet. Ved prædiktion læres filtre, medianer, middelværdier, standardafvigelser, PCA og screening kun på træning.",
        ),
        (
            tr(
                "Una operación no supervisada también puede filtrar información de validación.",
                "An unsupervised operation can still leak validation information.",
                "En usuperviseret operation kan stadig lække valideringsinformation.",
            ),
            tr(
                "La imputación simple es didáctica, no universal.",
                "Simple imputation is pedagogical, not universal.",
                "Simpel imputering er pædagogisk, ikke universel.",
            ),
        ),
    ),
    (
        "interpretation",
        tr(
            "PCA, lote, cribado y reporte",
            "PCA, batch, screening, and reporting",
            "PCA, batch, screening og rapportering",
        ),
        tr(
            "Relaciona scores con metadatos para detectar lote antes de interpretar enfermedad. El cribado univariante requiere multiplicidad y validación; una lista superior no equivale a biomarcadores. El informe individual separa datos, decisiones, resultados, limitaciones y siguientes pasos. Ollama puede revisar claridad, pero no la corrección numérica ni el dominio.",
            "Relate scores to metadata to detect batch before interpreting disease. Univariate screening requires multiplicity control and validation; a top list is not a biomarker set. The individual report separates data, decisions, results, limitations, and next steps. Ollama may review clarity, but not numerical correctness or mastery.",
            "Relatér scores til metadata for at opdage batch før sygdom fortolkes. Univariat screening kræver multiplicitetskontrol og validering; en topliste er ikke et biomarkørsæt. Den individuelle rapport adskiller data, beslutninger, resultater, begrænsninger og næste skridt. Ollama må gennemgå klarhed, men ikke numerisk korrekthed eller mestring.",
        ),
        (
            tr(
                "Separación en PCA es exploratoria, no causal.",
                "PCA separation is exploratory, not causal.",
                "Adskillelse i PCA er eksplorativ, ikke kausal.",
            ),
            tr(
                "La evidencia clínica exige datos y validación externos.",
                "Clinical evidence requires external data and validation.",
                "Klinisk evidens kræver eksterne data og validering.",
            ),
        ),
    ),
)

PRACTICES = (
    (
        "m12.p01",
        "PIPELINE_DESIGN",
        tr(
            "Define un contrato para matriz, metadatos y diccionario de datos.",
            "Define a contract for matrix, metadata, and data dictionary.",
            "Definér en kontrakt for matrix, metadata og dataordbog.",
        ),
        (
            tr(
                "Incluye clave, unidad, versión y códigos de ausencia.",
                "Include key, unit, version, and missing codes.",
                "Medtag nøgle, enhed, version og koder for manglende værdier.",
            ),
        ),
        tr(
            "Una fila por paciente, clave única, columnas proteicas numéricas y metadatos separados.",
            "One row per patient, unique key, numeric protein columns, and separate metadata.",
            "Én række pr. patient, entydig nøgle, numeriske proteinkolonner og separate metadata.",
        ),
        tr(
            "El contrato evita desalineación silenciosa.",
            "The contract prevents silent misalignment.",
            "Kontrakten forhindrer skjult fejljustering.",
        ),
        "",
    ),
    (
        "m12.p02",
        "DATA_INTERPRETATION",
        tr(
            "Distingue ausencia por paciente y por proteína y propone umbrales previos.",
            "Distinguish patient and protein missingness and propose prior thresholds.",
            "Skeln mellem manglende værdier pr. patient og protein og foreslå forudgående tærskler.",
        ),
        (
            tr(
                "No optimices umbrales por separación visual.",
                "Do not optimise thresholds by visual separation.",
                "Optimér ikke tærskler efter visuel adskillelse.",
            ),
        ),
        tr(
            "Reporta ambas distribuciones y justifica reglas antes de usar grupos.",
            "Report both distributions and justify rules before using groups.",
            "Rapportér begge fordelinger og begrund regler før grupper bruges.",
        ),
        tr(
            "Las dos direcciones de ausencia tienen consecuencias distintas.",
            "The two missingness directions have different consequences.",
            "De to retninger af manglende værdier har forskellige konsekvenser.",
        ),
        "",
    ),
    (
        "m12.p03",
        "PIPELINE_DESIGN",
        tr(
            "Ordena filtrado, imputación, log2, escalado y PCA para exploración y predicción.",
            "Order filtering, imputation, log2, scaling, and PCA for exploration and prediction.",
            "Ordén filtrering, imputering, log2, skalering og PCA til eksploration og prædiktion.",
        ),
        (
            tr(
                "En predicción, aprende todo dentro de entrenamiento.",
                "For prediction, learn everything within training.",
                "Ved prædiktion læres alt inden for træning.",
            ),
        ),
        tr(
            "Exploración: documentar y aplicar al conjunto; predicción: ajustar cada paso en entrenamiento y proyectar validación.",
            "Exploration: document and apply to the set; prediction: fit each step on training and project validation.",
            "Eksploration: dokumentér og anvend på sættet; prædiktion: tilpas hvert trin på træning og projicér validering.",
        ),
        tr(
            "La diferencia evita fuga.",
            "The distinction prevents leakage.",
            "Forskellen forhindrer lækage.",
        ),
        "",
    ),
    (
        "m12.p04",
        "DATA_INTERPRETATION",
        tr(
            "PC1 separa lotes y solo débilmente enfermedad. Redacta una conclusión.",
            "PC1 separates batches and only weakly disease. Write a conclusion.",
            "PC1 adskiller batches og kun svagt sygdom. Skriv en konklusion.",
        ),
        (
            tr(
                "Prioriza la explicación técnica.",
                "Prioritise the technical explanation.",
                "Prioritér den tekniske forklaring.",
            ),
        ),
        tr(
            "La principal variación está asociada con lote; cualquier contraste de enfermedad requiere ajuste, sensibilidad y validación.",
            "The main variation is associated with batch; disease contrasts require adjustment, sensitivity, and validation.",
            "Hovedvariationen er associeret med batch; sygdomskontraster kræver justering, følsomhed og validering.",
        ),
        tr(
            "PCA no demuestra causalidad.",
            "PCA does not prove causality.",
            "PCA beviser ikke kausalitet.",
        ),
        "",
    ),
    (
        "m12.p05",
        "DATA_INTERPRETATION",
        tr(
            "Evalúa una lista de 10 proteínas seleccionada entre 240.",
            "Evaluate a list of 10 proteins selected from 240.",
            "Vurdér en liste med 10 proteiner valgt blandt 240.",
        ),
        (
            tr(
                "Considera multiplicidad y validación.",
                "Consider multiplicity and validation.",
                "Overvej multiplicitet og validering.",
            ),
        ),
        tr(
            "Es un cribado exploratorio; reporta universo, criterio, incertidumbre, multiplicidad y rendimiento fuera de muestra.",
            "It is exploratory screening; report the universe, criterion, uncertainty, multiplicity, and out-of-sample performance.",
            "Det er eksplorativ screening; rapportér univers, kriterium, usikkerhed, multiplicitet og out-of-sample-ydeevne.",
        ),
        tr(
            "Una lista superior no es un panel clínico.",
            "A top list is not a clinical panel.",
            "En topliste er ikke et klinisk panel.",
        ),
        "",
    ),
    (
        "m12.p06",
        "ORAL_EXPLANATION",
        tr(
            "Presenta individualmente el caso en dos minutos: datos, decisiones, hallazgo, límite y siguiente paso.",
            "Present the case individually in two minutes: data, decisions, finding, limitation, and next step.",
            "Præsentér casen individuelt på to minutter: data, beslutninger, fund, begrænsning og næste skridt.",
        ),
        (
            tr(
                "Ollama puede revisar claridad, no números.",
                "Ollama may review clarity, not numbers.",
                "Ollama må gennemgå klarhed, ikke tal.",
            ),
        ),
        tr(
            "Explica matriz sintética 48x240, QC, PCA dominado por lote, cribado en entrenamiento y necesidad de datos externos.",
            "Explain the synthetic 48x240 matrix, QC, batch-dominated PCA, training-only screening, and need for external data.",
            "Forklar den syntetiske 48x240-matrix, QC, batchdomineret PCA, screening kun på træning og behovet for eksterne data.",
        ),
        tr(
            "La revisión lingüística no modifica corrección ni dominio.",
            "Language review does not change correctness or mastery.",
            "Sproglig gennemgang ændrer ikke korrekthed eller mestring.",
        ),
        "",
    ),
)
