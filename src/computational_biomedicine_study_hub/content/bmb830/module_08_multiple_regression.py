"""BMB830 module 8: multiple regression and design matrices."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m08",
    title=(
        "Regresión múltiple y matriz de diseño",
        "Multiple regression and the design matrix",
        "Multipel regression og designmatrixen",
    ),
    summary=(
        "Construye modelos lineales con varios predictores, interpreta efectos ajustados, codifica variables categóricas y distingue ajuste por confusión de control automático de sesgo.",
        "Build linear models with several predictors, interpret adjusted effects, encode categorical variables, and distinguish confounding adjustment from automatic bias control.",
        "Opbyg lineære modeller med flere prædiktorer, fortolk justerede effekter, kod kategoriske variable, og skeln mellem justering for confounding og automatisk kontrol af bias.",
    ),
    objectives=(
        (
            "m08.o1",
            (
                "Expresar e interpretar un modelo lineal múltiple como una media condicional.",
                "Express and interpret a multiple linear model as a conditional mean.",
                "Udtrykke og fortolke en multipel lineær model som en betinget middelværdi.",
            ),
        ),
        (
            "m08.o2",
            (
                "Construir e inspeccionar una matriz de diseño con predictores continuos y categóricos.",
                "Construct and inspect a design matrix with continuous and categorical predictors.",
                "Konstruere og inspicere en designmatrix med kontinuerte og kategoriske prædiktorer.",
            ),
        ),
        (
            "m08.o3",
            (
                "Interpretar coeficientes ajustados, niveles de referencia e indicadores con sus unidades.",
                "Interpret adjusted coefficients, reference levels, and indicator variables with their units.",
                "Fortolke justerede koefficienter, referenceniveauer og indikatorvariable med deres enheder.",
            ),
        ),
        (
            "m08.o4",
            (
                "Distinguir confusión, precisión, colinealidad y sobreajuste al seleccionar covariables.",
                "Distinguish confounding, precision, collinearity, and overfitting when selecting covariates.",
                "Skelne mellem confounding, præcision, kollinearitet og overtilpasning ved valg af kovariater.",
            ),
        ),
    ),
    concepts=(
        (
            "conditional-model",
            (
                "Modelo lineal múltiple",
                "Multiple linear model",
                "Multipel lineær model",
            ),
            (
                "El modelo E(Y|X,Z)=β0+β1X+β2Z describe la media esperada de Y para valores concretos de X y Z. β1 representa el cambio medio esperado en Y por una unidad de X manteniendo Z constante dentro del modelo; no es automáticamente un efecto causal.",
                "The model E(Y|X,Z)=β0+β1X+β2Z describes the expected mean of Y at specified values of X and Z. β1 is the expected mean change in Y for one unit of X while holding Z fixed within the model; it is not automatically a causal effect.",
                "Modellen E(Y|X,Z)=β0+β1X+β2Z beskriver den forventede middelværdi af Y ved bestemte værdier af X og Z. β1 er den forventede ændring i Y ved én enheds ændring i X, mens Z holdes fast i modellen; den er ikke automatisk en kausal effekt.",
            ),
            (
                (
                    "Cada coeficiente es condicional a los demás términos incluidos.",
                    "Each coefficient is conditional on the other included terms.",
                    "Hver koefficient er betinget af de øvrige inkluderede led.",
                ),
                (
                    "La interpretación depende de escala, codificación y población analizada.",
                    "Interpretation depends on scale, coding, and the analysed population.",
                    "Fortolkningen afhænger af skala, kodning og den analyserede population.",
                ),
            ),
        ),
        (
            "design-matrix",
            (
                "Matriz de diseño",
                "Design matrix",
                "Designmatrix",
            ),
            (
                "La matriz de diseño contiene una fila por unidad analítica y una columna por parámetro estimado: intercepto, predictores continuos e indicadores derivados de factores. El rango completo de la matriz es necesario para estimar coeficientes únicos.",
                "The design matrix contains one row per analysis unit and one column per estimated parameter: intercept, continuous predictors, and indicators derived from factors. Full matrix rank is required for unique coefficient estimates.",
                "Designmatrixen indeholder én række pr. analyseenhed og én kolonne pr. estimeret parameter: skæring, kontinuerte prædiktorer og indikatorer afledt af faktorer. Fuld matrixrang kræves for entydige koefficientestimater.",
            ),
            (
                (
                    "`model.matrix()` hace visible la codificación usada por R.",
                    "`model.matrix()` makes R's coding visible.",
                    "`model.matrix()` gør R's kodning synlig.",
                ),
                (
                    "Una columna redundante produce dependencia lineal y coeficientes no identificables.",
                    "A redundant column creates linear dependence and non-identifiable coefficients.",
                    "En redundant kolonne skaber lineær afhængighed og ikke-identificerbare koefficienter.",
                ),
            ),
        ),
        (
            "categorical-predictors",
            (
                "Factores y nivel de referencia",
                "Factors and the reference level",
                "Faktorer og referenceniveau",
            ),
            (
                "Con un factor de K niveles y un intercepto, R crea K−1 indicadores. El intercepto corresponde a la media esperada del nivel de referencia cuando los predictores continuos valen cero. Cada coeficiente de nivel compara ese nivel con la referencia, manteniendo constantes los demás predictores.",
                "With a K-level factor and an intercept, R creates K−1 indicators. The intercept is the expected mean for the reference level when continuous predictors equal zero. Each level coefficient compares that level with the reference while holding other predictors fixed.",
                "Med en faktor med K niveauer og en skæring opretter R K−1 indikatorer. Skæringen er den forventede middelværdi for referenceniveauet, når kontinuerte prædiktorer er nul. Hver niveaukoefficient sammenligner niveauet med referencen, mens øvrige prædiktorer holdes faste.",
            ),
            (
                (
                    "Cambiar la referencia cambia los coeficientes, no las predicciones ajustadas.",
                    "Changing the reference changes coefficients, not fitted predictions.",
                    "Et skift af reference ændrer koefficienterne, ikke de tilpassede prædiktioner.",
                ),
                (
                    "Centrar predictores continuos puede volver interpretable el intercepto.",
                    "Centring continuous predictors can make the intercept interpretable.",
                    "Centrering af kontinuerte prædiktorer kan gøre skæringen fortolkelig.",
                ),
            ),
        ),
        (
            "confounding-collinearity",
            (
                "Confusión, ajuste y colinealidad",
                "Confounding, adjustment, and collinearity",
                "Confounding, justering og kollinearitet",
            ),
            (
                "Una variable confusora está relacionada con la exposición y el resultado y no debe ser consecuencia de la exposición. Ajustarla puede cambiar la estimación de interés. Incluir variables por disponibilidad no garantiza control de confusión y puede introducir sobreajuste, sesgo de selección o colinealidad.",
                "A confounder is related to exposure and outcome and should not be caused by the exposure. Adjusting for it can change the target estimate. Including variables merely because they are available does not guarantee confounding control and may introduce overfitting, selection bias, or collinearity.",
                "En confounder er relateret til eksponering og udfald og bør ikke være forårsaget af eksponeringen. Justering kan ændre målestimatet. At inkludere variable alene fordi de er tilgængelige garanterer ikke kontrol af confounding og kan skabe overtilpasning, selektionsbias eller kollinearitet.",
            ),
            (
                (
                    "La selección de covariables debe basarse en la pregunta y el conocimiento causal.",
                    "Covariate selection should follow the question and causal knowledge.",
                    "Valg af kovariater bør følge spørgsmålet og kausal viden.",
                ),
                (
                    "La colinealidad aumenta incertidumbre aunque el ajuste global parezca bueno.",
                    "Collinearity increases uncertainty even when overall fit appears good.",
                    "Kollinearitet øger usikkerheden, selv når den samlede tilpasning ser god ud.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m08.e01",
            (
                "Asociación cruda y efecto ajustado",
                "Crude association and adjusted effect",
                "Ujusteret association og justeret effekt",
            ),
            (
                "Compara el coeficiente de exposición antes y después de ajustar por edad en datos sintéticos.",
                "Compare the exposure coefficient before and after adjustment for age in synthetic data.",
                "Sammenlign eksponeringskoefficienten før og efter justering for alder i syntetiske data.",
            ),
            (
                (
                    "Edad se relaciona con exposición y respuesta en estos datos.",
                    "Age is related to exposure and response in these data.",
                    "Alder er relateret til eksponering og respons i disse data.",
                ),
                (
                    "El coeficiente ajustado compara unidades de la misma edad modelada.",
                    "The adjusted coefficient compares units at the same modelled age.",
                    "Den justerede koefficient sammenligner enheder ved samme modellerede alder.",
                ),
            ),
            """exposure <- c(1, 2, 2, 3, 4, 4, 5, 6)
age <- c(30, 34, 39, 42, 48, 53, 57, 62)
response <- c(5.2, 6.1, 6.8, 7.4, 8.8, 9.2, 10.1, 11.0)
crude <- lm(response ~ exposure)
adjusted <- lm(response ~ exposure + age)
cat(sprintf("crude_exposure=%.3f\n", coef(crude)[["exposure"]]))
cat(sprintf("adjusted_exposure=%.3f\n", coef(adjusted)[["exposure"]]))
cat(sprintf("adjusted_age=%.3f", coef(adjusted)[["age"]]))
""",
            """crude_exposure=1.165
adjusted_exposure=0.643
adjusted_age=0.055""",
            (
                "La diferencia entre coeficientes muestra que la asociación cruda mezclaba exposición y edad. El modelo por sí solo no demuestra que el coeficiente ajustado sea causal.",
                "The coefficient difference shows that the crude association mixed exposure and age. The model alone does not prove that the adjusted coefficient is causal.",
                "Forskellen mellem koefficienterne viser, at den ujusterede association blandede eksponering og alder. Modellen alene beviser ikke, at den justerede koefficient er kausal.",
            ),
        ),
        (
            "m08.e02",
            (
                "Factor y matriz de diseño",
                "Factor and design matrix",
                "Faktor og designmatrix",
            ),
            (
                "Inspecciona cómo R codifica tres grupos y ajusta sus diferencias respecto a control.",
                "Inspect how R encodes three groups and fits their differences from control.",
                "Inspicér hvordan R koder tre grupper og tilpasser deres forskelle fra kontrol.",
            ),
            (
                (
                    "Control se fija como nivel de referencia.",
                    "Control is set as the reference level.",
                    "Kontrol sættes som referenceniveau.",
                ),
                (
                    "La matriz contiene dos indicadores, no tres, además del intercepto.",
                    "The matrix contains two indicators, not three, in addition to the intercept.",
                    "Matrixen indeholder to indikatorer, ikke tre, ud over skæringen.",
                ),
            ),
            """group <- factor(
  c("control", "control", "A", "A", "B", "B"),
  levels = c("control", "A", "B")
)
age <- c(40, 44, 41, 46, 42, 47)
response <- c(7.0, 7.3, 8.0, 8.4, 9.1, 9.3)
fit <- lm(response ~ group + age)
X <- model.matrix(fit)
cat(paste(colnames(X), collapse = ","), "\n")
cat(sprintf("groupA=%.2f\n", coef(fit)[["groupA"]]))
cat(sprintf("groupB=%.2f", coef(fit)[["groupB"]]))
""",
            """(Intercept),groupA,groupB,age
groupA=0.89
groupB=1.82""",
            (
                "Los coeficientes de A y B son diferencias ajustadas respecto a control. Cambiar la referencia reexpresaría los contrastes sin cambiar los valores ajustados.",
                "The A and B coefficients are adjusted differences from control. Changing the reference would re-express the contrasts without changing fitted values.",
                "Koefficienterne for A og B er justerede forskelle fra kontrol. Et skift af reference ville omformulere kontrasterne uden at ændre de tilpassede værdier.",
            ),
        ),
    ),
    practices=(
        (
            "m08.p01",
            "DATA_INTERPRETATION",
            (
                "Interpreta βexposición=0,8 en Y~exposición+edad.",
                "Interpret βexposure=0.8 in Y~exposure+age.",
                "Fortolk βeksponering=0,8 i Y~eksponering+alder.",
            ),
            (("Mantén edad constante dentro del modelo.", "Hold age fixed within the model.", "Hold alder fast i modellen."),),
            (
                "Por cada unidad adicional de exposición, la media esperada de Y aumenta 0,8 unidades al comparar observaciones con la misma edad modelada.",
                "For each additional exposure unit, expected mean Y increases by 0.8 units when comparing observations at the same modelled age.",
                "For hver ekstra eksponeringsenhed stiger den forventede middelværdi af Y med 0,8 enheder ved sammenligning af observationer med samme modellerede alder.",
            ),
            (
                "Es una interpretación condicional y no implica causalidad automáticamente.",
                "This is a conditional interpretation and does not automatically imply causation.",
                "Dette er en betinget fortolkning og indebærer ikke automatisk kausalitet.",
            ),
            "",
        ),
        (
            "m08.p02",
            "CODE_COMPLETION",
            (
                "Completa un modelo con respuesta, exposición, edad y grupo.",
                "Complete a model with response, exposure, age, and group.",
                "Fuldfør en model med respons, eksponering, alder og gruppe.",
            ),
            (("Usa una fórmula de lm.", "Use an lm formula.", "Brug en lm-formel."),),
            ("lm(response ~ exposure + age + group, data = data)",) * 3,
            (
                "Cada término aditivo obtiene un coeficiente condicionado a los demás.",
                "Each additive term receives a coefficient conditional on the others.",
                "Hvert additivt led får en koefficient betinget af de øvrige.",
            ),
            "fit <- __________________________________________",
        ),
        (
            "m08.p03",
            "DEBUGGING",
            (
                "Corrige una matriz que incluye intercepto y un indicador para cada uno de tres niveles.",
                "Correct a matrix containing an intercept and one indicator for each of three levels.",
                "Ret en matrix med skæring og én indikator for hvert af tre niveauer.",
            ),
            (("Existe una combinación lineal exacta.", "There is an exact linear combination.", "Der findes en eksakt lineær kombination."),),
            (
                "Conservar el intercepto y omitir un indicador como referencia, o eliminar el intercepto si se desean tres medias de grupo explícitas.",
                "Keep the intercept and omit one indicator as reference, or remove the intercept when three explicit group means are desired.",
                "Behold skæringen og udelad én indikator som reference, eller fjern skæringen, hvis tre eksplicitte gruppemiddelværdier ønskes.",
            ),
            (
                "Intercepto más todos los indicadores produce rango deficiente.",
                "An intercept plus every indicator produces rank deficiency.",
                "En skæring plus alle indikatorer giver rangmangel.",
            ),
            "",
        ),
        (
            "m08.p04",
            "PIPELINE_DESIGN",
            (
                "Diseña un análisis para estimar la asociación exposición–respuesta ajustada por confusión.",
                "Design an analysis to estimate the exposure–response association adjusted for confounding.",
                "Design en analyse til at estimere eksponering–respons-associationen justeret for confounding.",
            ),
            (("Selecciona covariables antes del ajuste.", "Select covariates before fitting.", "Vælg kovariater før tilpasning."),),
            (
                "Definir estimando y unidad; justificar covariables con conocimiento causal; inspeccionar codificación y datos faltantes; ajustar modelo; evaluar estimación, intervalo, residuos, colinealidad y sensibilidad.",
                "Define estimand and unit; justify covariates using causal knowledge; inspect coding and missing data; fit the model; evaluate estimate, interval, residuals, collinearity, and sensitivity.",
                "Definér estimand og enhed; begrund kovariater med kausal viden; inspicér kodning og manglende data; tilpas modellen; vurder estimat, interval, residualer, kollinearitet og følsomhed.",
            ),
            (
                "Agregar todas las variables disponibles no sustituye una estrategia de ajuste.",
                "Adding every available variable is not an adjustment strategy.",
                "At tilføje alle tilgængelige variable er ikke en justeringsstrategi.",
            ),
            "",
        ),
        (
            "m08.p05",
            "ORAL_EXPLANATION",
            (
                "Explica qué cambia y qué no cambia al modificar el nivel de referencia.",
                "Explain what changes and what does not when the reference level changes.",
                "Forklar hvad der ændres og ikke ændres, når referenceniveauet skiftes.",
            ),
            (("Distingue parametrización de ajuste.", "Distinguish parameterisation from fit.", "Skeln mellem parametrisering og tilpasning."),),
            (
                "Cambian intercepto y coeficientes de contraste porque se expresan comparaciones distintas; no cambian valores ajustados, residuos ni ajuste global del mismo modelo.",
                "The intercept and contrast coefficients change because different comparisons are expressed; fitted values, residuals, and overall fit of the same model do not change.",
                "Skæringen og kontrastkoefficienterne ændres, fordi andre sammenligninger udtrykkes; tilpassede værdier, residualer og samlet tilpasning ændres ikke.",
            ),
            (
                "La referencia debe elegirse por interpretabilidad, no para obtener significación.",
                "The reference should be chosen for interpretability, not to obtain significance.",
                "Referencen bør vælges for fortolkelighed, ikke for at opnå signifikans.",
            ),
            "",
        ),
        (
            "m08.p06",
            "DATA_INTERPRETATION",
            (
                "Interpreta dos predictores casi idénticos con intervalos muy amplios.",
                "Interpret two nearly identical predictors with very wide intervals.",
                "Fortolk to næsten identiske prædiktorer med meget brede intervaller.",
            ),
            (("Piensa en información redundante.", "Think about redundant information.", "Tænk på redundant information."),),
            (
                "La colinealidad dificulta separar sus contribuciones y aumenta la incertidumbre individual de los coeficientes, aunque las predicciones combinadas puedan mantenerse estables.",
                "Collinearity makes their separate contributions difficult to identify and increases coefficient uncertainty even when combined predictions remain stable.",
                "Kollinearitet gør det vanskeligt at adskille deres bidrag og øger koefficientusikkerheden, selv når kombinerede prædiktioner er stabile.",
            ),
            (
                "No debe resolverse eliminando automáticamente una variable sin considerar la pregunta científica.",
                "It should not be resolved by automatically deleting a variable without considering the scientific question.",
                "Det bør ikke løses ved automatisk at slette en variabel uden at overveje det videnskabelige spørgsmål.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            ("¿Qué representa β1 en Y~X+Z?", "What does β1 represent in Y~X+Z?", "Hvad repræsenterer β1 i Y~X+Z?"),
            (("a", ("Cambio medio en Y por unidad de X manteniendo Z constante", "Mean Y change per X unit holding Z fixed", "Ændring i middel-Y pr. X-enhed med Z holdt fast")), ("b", ("Correlación entre X y Z", "Correlation between X and Z", "Korrelation mellem X og Z")), ("c", ("Efecto causal garantizado", "Guaranteed causal effect", "Garanteret kausal effekt")), ("d", ("Varianza residual", "Residual variance", "Residualvarians"))),
            "a",
            ("Es un contraste condicional dentro del modelo.", "It is a conditional contrast within the model.", "Det er en betinget kontrast i modellen."),
        ),
        (
            "002",
            ("¿Cuántos indicadores crea un factor de 4 niveles con intercepto?", "How many indicators does a 4-level factor create with an intercept?", "Hvor mange indikatorer skaber en faktor med 4 niveauer og en skæring?"),
            (("a", ("1", "1", "1")), ("b", ("2", "2", "2")), ("c", ("3", "3", "3")), ("d", ("4", "4", "4"))),
            "c",
            ("Un nivel actúa como referencia.", "One level acts as reference.", "Ét niveau fungerer som reference."),
        ),
        (
            "003",
            ("¿Qué función muestra la codificación del modelo?", "Which function displays model coding?", "Hvilken funktion viser modelkodningen?"),
            (("a", ("model.matrix", "model.matrix", "model.matrix")), ("b", ("mean", "mean", "mean")), ("c", ("table", "table", "table")), ("d", ("sample", "sample", "sample"))),
            "a",
            ("`model.matrix()` devuelve las columnas usadas para estimar parámetros.", "`model.matrix()` returns columns used to estimate parameters.", "`model.matrix()` returnerer kolonnerne, der bruges til at estimere parametre."),
        ),
        (
            "004",
            ("¿Qué cambia al elegir otra referencia?", "What changes when another reference is chosen?", "Hvad ændres, når en anden reference vælges?"),
            (("a", ("Parametrización de coeficientes", "Coefficient parameterisation", "Koefficientparametrisering")), ("b", ("Valores ajustados", "Fitted values", "Tilpassede værdier")), ("c", ("Residuos", "Residuals", "Residualer")), ("d", ("Número de observaciones", "Number of observations", "Antal observationer"))),
            "a",
            ("Las mismas predicciones se expresan con contrastes distintos.", "The same predictions are expressed through different contrasts.", "De samme prædiktioner udtrykkes gennem andre kontraster."),
        ),
        (
            "005",
            ("¿Qué puede indicar intervalos amplios para predictores muy relacionados?", "What may wide intervals for strongly related predictors indicate?", "Hvad kan brede intervaller for stærkt relaterede prædiktorer indikere?"),
            (("a", ("Colinealidad", "Collinearity", "Kollinearitet")), ("b", ("Causalidad", "Causation", "Kausalitet")), ("c", ("Mayor n efectivo", "Larger effective n", "Større effektivt n")), ("d", ("Ausencia de error", "Absence of error", "Fravær af fejl"))),
            "a",
            ("La información redundante dificulta separar coeficientes.", "Redundant information makes coefficients difficult to separate.", "Redundant information gør koefficienter svære at adskille."),
        ),
        (
            "006",
            ("¿Cómo debe seleccionarse una covariable de ajuste?", "How should an adjustment covariate be selected?", "Hvordan bør en justeringskovariat vælges?"),
            (("a", ("Según pregunta y conocimiento causal", "By question and causal knowledge", "Efter spørgsmål og kausal viden")), ("b", ("Solo por p<0,05", "Only by p<0.05", "Kun efter p<0,05")), ("c", ("Por disponibilidad", "By availability", "Efter tilgængelighed")), ("d", ("Después de probar todos los modelos", "After testing every model", "Efter at have testet alle modeller"))),
            "a",
            ("El ajuste debe corresponder al estimando y al mecanismo causal supuesto.", "Adjustment should match the estimand and assumed causal mechanism.", "Justering bør passe til estimanden og den antagede kausale mekanisme."),
        ),
        (
            "007",
            ("¿Qué significa un coeficiente groupB?", "What does a groupB coefficient mean?", "Hvad betyder en groupB-koefficient?"),
            (("a", ("Diferencia B–referencia ajustada", "Adjusted B-minus-reference difference", "Justeret forskel B minus reference")), ("b", ("Media absoluta de B", "Absolute mean of B", "Absolut middelværdi for B")), ("c", ("Varianza de B", "Variance of B", "Varians for B")), ("d", ("Comparación B–todos", "B-versus-all comparison", "Sammenligning B mod alle"))),
            "a",
            ("La interpretación depende del nivel de referencia y de los demás términos.", "Interpretation depends on the reference level and other terms.", "Fortolkningen afhænger af referenceniveauet og de øvrige led."),
        ),
        (
            "008",
            ("¿Qué riesgo tiene incluir demasiados predictores con pocos datos?", "What is a risk of too many predictors with little data?", "Hvad er en risiko ved for mange prædiktorer og få data?"),
            (("a", ("Sobreajuste e inestabilidad", "Overfitting and instability", "Overtilpasning og ustabilitet")), ("b", ("Causalidad automática", "Automatic causality", "Automatisk kausalitet")), ("c", ("Mayor potencia garantizada", "Guaranteed higher power", "Garanteret højere styrke")), ("d", ("Eliminación de sesgo", "Bias elimination", "Eliminering af bias"))),
            "a",
            ("Cada parámetro consume información y puede aumentar varianza.", "Each parameter consumes information and may increase variance.", "Hver parameter bruger information og kan øge variansen."),
        ),
    ),
    true_false=(
        ("009", ("Un coeficiente ajustado es automáticamente causal.", "An adjusted coefficient is automatically causal.", "En justeret koefficient er automatisk kausal."), False, ("La causalidad requiere diseño y supuestos adicionales.", "Causality requires additional design and assumptions.", "Kausalitet kræver yderligere design og antagelser.")),
        ("010", ("Con intercepto, un factor de K niveles usa K−1 indicadores.", "With an intercept, a K-level factor uses K−1 indicators.", "Med en skæring bruger en faktor med K niveauer K−1 indikatorer."), True, ("El nivel omitido es la referencia.", "The omitted level is the reference.", "Det udeladte niveau er referencen.")),
        ("011", ("Cambiar la referencia cambia los valores ajustados.", "Changing the reference changes fitted values.", "Et skift af reference ændrer de tilpassede værdier."), False, ("Solo cambia la parametrización del mismo ajuste.", "Only the parameterisation of the same fit changes.", "Kun parametrisering af samme tilpasning ændres.")),
        ("012", ("La matriz de diseño tiene una fila por unidad analítica.", "The design matrix has one row per analysis unit.", "Designmatrixen har én række pr. analyseenhed."), True, ("Las columnas representan términos estimables.", "Columns represent estimable terms.", "Kolonner repræsenterer estimerbare led.")),
        ("013", ("Agregar todas las variables disponibles garantiza control de confusión.", "Adding all available variables guarantees confounding control.", "At tilføje alle tilgængelige variable garanterer kontrol af confounding."), False, ("La selección incorrecta puede introducir sesgo o inestabilidad.", "Incorrect selection can introduce bias or instability.", "Forkert valg kan skabe bias eller ustabilitet.")),
        ("014", ("La colinealidad puede ampliar intervalos de coeficientes.", "Collinearity can widen coefficient intervals.", "Kollinearitet kan gøre koefficientintervaller bredere."), True, ("Reduce la información independiente para separar efectos.", "It reduces independent information for separating effects.", "Den reducerer uafhængig information til at adskille effekter.")),
        ("015", ("Centrar edad puede hacer más interpretable el intercepto.", "Centring age can make the intercept more interpretable.", "Centrering af alder kan gøre skæringen mere fortolkelig."), True, ("El cero pasa a representar el valor de centrado.", "Zero then represents the centring value.", "Nul repræsenterer derefter centreringsværdien.")),
        ("016", ("Rango deficiente permite estimar todos los coeficientes de forma única.", "Rank deficiency allows every coefficient to be uniquely estimated.", "Rangmangel gør det muligt at estimere alle koefficienter entydigt."), False, ("La dependencia lineal impide identificación única.", "Linear dependence prevents unique identification.", "Lineær afhængighed forhindrer entydig identifikation.")),
    ),
    tutor=(
        (
            "La regresión múltiple representa medias condicionales mediante una matriz de diseño. Los coeficientes deben interpretarse según escala, referencia y términos incluidos; el ajuste por covariables requiere una justificación científica y no convierte asociaciones en efectos causales.",
            "Multiple regression represents conditional means through a design matrix. Coefficients must be interpreted according to scale, reference, and included terms; covariate adjustment requires scientific justification and does not turn associations into causal effects.",
            "Multipel regression repræsenterer betingede middelværdier gennem en designmatrix. Koefficienter skal fortolkes efter skala, reference og inkluderede led; justering for kovariater kræver videnskabelig begrundelse og gør ikke associationer kausale.",
        ),
        (
            ("Los coeficientes son condicionales.", "Coefficients are conditional.", "Koefficienter er betingede."),
            ("La matriz de diseño determina qué se estima.", "The design matrix determines what is estimated.", "Designmatrixen bestemmer, hvad der estimeres."),
            ("Los factores requieren una referencia o una parametrización alternativa.", "Factors require a reference or an alternative parameterisation.", "Faktorer kræver en reference eller en alternativ parametrisering."),
            ("El ajuste causal depende de selección de covariables defendible.", "Causal adjustment depends on defensible covariate selection.", "Kausal justering afhænger af et forsvarligt valg af kovariater."),
        ),
        (
            ("Interpretar ajuste como causalidad automática.", "Interpreting adjustment as automatic causality.", "At fortolke justering som automatisk kausalitet."),
            ("Ignorar el nivel de referencia.", "Ignoring the reference level.", "At ignorere referenceniveauet."),
            ("Seleccionar variables solo por valores p.", "Selecting variables only by p-values.", "At vælge variable alene efter p-værdier."),
        ),
        (
            ("¿Cuál es el estimando ajustado?", "What is the adjusted estimand?", "Hvad er den justerede estimand?"),
            ("¿Cómo está codificado cada predictor?", "How is each predictor coded?", "Hvordan er hver prædiktor kodet?"),
            ("¿Qué variable actúa como referencia?", "Which variable level is the reference?", "Hvilket variabelniveau er reference?"),
        ),
        (
            ("Interpreta coeficientes de forma condicional.", "Interprets coefficients conditionally.", "Fortolker koefficienter betinget."),
            ("Reconstruye la matriz de diseño.", "Reconstructs the design matrix.", "Rekonstruerer designmatrixen."),
            ("Justifica ajuste y reconoce colinealidad.", "Justifies adjustment and recognises collinearity.", "Begrunder justering og genkender kollinearitet."),
        ),
        (
            ("No inventar causalidad a partir de ajuste estadístico.", "Do not invent causality from statistical adjustment.", "Udled ikke kausalitet alene fra statistisk justering."),
            ("No recomendar selección automática por significación.", "Do not recommend automatic significance-based selection.", "Anbefal ikke automatisk selektion efter signifikans."),
            ("Responder en el idioma activo.", "Respond in the active language.", "Svar på det aktive sprog."),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base stats documentation: lm and model.matrix",
            "Linear-model design-matrix and confounding principles",
        ),
    ),
)

LOCALIZED_MODULE_08_MULTIPLE_REGRESSION = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_08 = build_question_bank(_SPEC)
MODULE_08_MULTIPLE_REGRESSION: LearningModule = (
    LOCALIZED_MODULE_08_MULTIPLE_REGRESSION.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_08: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08
)


def materialize_module_08_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-8 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_08, locale)


__all__ = [
    "LOCALIZED_MODULE_08_MULTIPLE_REGRESSION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "MODULE_08_MULTIPLE_REGRESSION",
    "OBJECTIVE_QUESTION_BANK_08",
    "materialize_module_08_question_bank",
]
