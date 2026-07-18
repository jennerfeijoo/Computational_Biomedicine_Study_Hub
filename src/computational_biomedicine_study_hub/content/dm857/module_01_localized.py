"""Complete English and Danish localization of the authored DM857 module 1."""

from __future__ import annotations

from ...learning.activity_types import ActivityType
from ..localized_models import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedConceptBlock,
    LocalizedLearningModule,
    LocalizedLearningObjective,
    LocalizedPracticeExercise,
    LocalizedText,
    LocalizedTutorSupportPacket,
    LocalizedWorkedExample,
)
from .module_01_es import MODULE as _ES


def _t(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish=spanish, english=english, danish=danish)


def _same(text: str) -> LocalizedText:
    return _t(text, text, text)


def _option(
    option_id: str,
    spanish: str,
    english: str,
    danish: str,
) -> LocalizedAssessmentOption:
    return LocalizedAssessmentOption(option_id=option_id, text=_t(spanish, english, danish))


_OBJECTIVES_EN = (
    "Separate a concrete situation into inputs, transformations, constraints, and observable outputs.",
    "Distinguish precisely between expression, value, type, variable, assignment, and statement.",
    "Predict the value and type of arithmetic and text expressions before executing them.",
    "Represent program state using a variable trace table.",
    "Apply explicit conversions between int, float, and str when required by the problem.",
    "Differentiate syntax, runtime, and logic errors, and propose a minimal test to detect them.",
)
_OBJECTIVES_DA = (
    "Opdele en konkret situation i input, transformationer, begrænsninger og observerbare output.",
    "Skelne præcist mellem udtryk, værdi, type, variabel, tildeling og sætning.",
    "Forudsige værdien og typen af aritmetiske udtryk og tekstudtryk før de køres.",
    "Repræsentere programtilstanden med en tabel over variable efter hvert trin.",
    "Anvende eksplicitte konverteringer mellem int, float og str, når problemet kræver det.",
    "Skelne mellem syntaksfejl, kørselsfejl og logiske fejl samt foreslå en minimal test.",
)

_CONCEPT_TRANSLATIONS = (
    (
        "From problem to program",
        "Programming does not begin with syntax. It begins by building an operational representation of a problem. A real situation contains relevant and incidental details; the model retains only what is needed to produce a verifiable answer. An algorithm is then designed from the model as a finite and unambiguous sequence of steps. The program is a concrete implementation of that algorithm. Separating these layers lets us assess the model, algorithm, and code independently.",
        (
            "Problem, model, algorithm, and program are not synonyms.",
            "Inputs and outputs should be defined before coding.",
            "A constraint states which values are valid or which behaviour is expected.",
            "Correctness is judged against the problem specification.",
        ),
        "Fra problem til program",
        "Programmering begynder ikke med syntaks. Den begynder med at opbygge en operationel repræsentation af et problem. En virkelig situation indeholder både relevante og tilfældige detaljer; modellen bevarer kun det, der er nødvendigt for at give et efterprøveligt svar. Ud fra modellen designes en algoritme som en endelig og entydig række af trin. Programmet er en konkret implementering af algoritmen. Når lagene adskilles, kan model, algoritme og kode vurderes hver for sig.",
        (
            "Problem, model, algoritme og program er ikke synonymer.",
            "Input og output bør defineres før kodning.",
            "En begrænsning angiver gyldige værdier eller forventet adfærd.",
            "Korrekthed vurderes i forhold til problemspecifikationen.",
        ),
    ),
    (
        "Expressions, values, and types",
        "An expression combines literals, variables, operators, and calls that Python can evaluate to obtain a value. Every value has a type, and the type determines which operations are valid and how they are interpreted. For example, 3 + 4 produces the integer 7, whereas '3' + '4' produces the string '34'. Python is dynamically typed: a variable may refer to values of different types, although every value always has a defined type.",
        (
            "An expression is evaluated; a statement performs an action or changes state.",
            "int represents integers, float floating-point numbers, and str text.",
            "The / operator produces a float, even when division is exact.",
            "type() lets you inspect the type of a value.",
        ),
        "Udtryk, værdier og typer",
        "Et udtryk kombinerer literaler, variable, operatorer og kald, som Python kan evaluere for at få en værdi. Hver værdi har en type, og typen bestemmer, hvilke operationer der er gyldige, og hvordan de fortolkes. For eksempel giver 3 + 4 heltallet 7, mens '3' + '4' giver tekststrengen '34'. Python er dynamisk typet: en variabel kan henvise til værdier af forskellige typer, men hver værdi har altid en bestemt type.",
        (
            "Et udtryk evalueres; en sætning udfører en handling eller ændrer tilstanden.",
            "int repræsenterer heltal, float decimaltal og str tekst.",
            "Operatoren / giver en float, selv når divisionen går op.",
            "type() gør det muligt at undersøge en værdis type.",
        ),
    ),
    (
        "Variables, assignment, and state",
        "A variable is a name associated with a value. Assignment first evaluates the expression on the right and then binds the name on the left to the result. This is why x = x + 1 is valid in programming: it is a state update, not mathematical equality. Program state is the set of name-value associations at a particular moment. A trace table records each statement and the resulting state.",
        (
            "Assignment uses = and does not assert mathematical equality.",
            "The right-hand expression is evaluated before the left-hand variable changes.",
            "Names should describe the meaning of the data.",
            "Manual tracing helps reason about reassignment.",
        ),
        "Variable, tildeling og tilstand",
        "En variabel er et navn, der er knyttet til en værdi. Tildeling evaluerer først udtrykket til højre og knytter derefter navnet til venstre til resultatet. Derfor er x = x + 1 gyldig i programmering: det er en tilstandsopdatering og ikke matematisk lighed. Programtilstanden er mængden af navn-værdi-forbindelser på et bestemt tidspunkt. En gennemgangstabel registrerer hver sætning og den efterfølgende tilstand.",
        (
            "Tildeling bruger = og udtrykker ikke matematisk lighed.",
            "Udtrykket til højre evalueres, før variablen til venstre ændres.",
            "Navne bør beskrive dataenes betydning.",
            "Manuel gennemgang hjælper med at forstå gentildeling.",
        ),
    ),
    (
        "Operators, precedence, and conversion",
        "The basic arithmetic operators are +, -, *, /, //, %, and **. Python applies precedence rules: parentheses first, then exponentiation, then multiplication, division, floor division, and modulo, and finally addition and subtraction. Parentheses may change the order or clarify intent. int(), float(), and str() create values of another type when conversion is possible. Conversion may lose information: int(4.9) produces 4, not 5.",
        (
            "// performs floor division; % returns the remainder.",
            "** represents exponentiation; ^ is not exponentiation.",
            "Precedence can be changed with parentheses.",
            "Every conversion should be justified by the intended meaning of the data.",
        ),
        "Operatorer, præcedens og konvertering",
        "De grundlæggende aritmetiske operatorer er +, -, *, /, //, % og **. Python anvender præcedensregler: først parenteser, derefter potens, så multiplikation, division, heltalsdivision og modulo, og til sidst addition og subtraktion. Parenteser kan ændre rækkefølgen eller tydeliggøre hensigten. int(), float() og str() opretter værdier af en anden type, når konverteringen er mulig. Konvertering kan miste information: int(4.9) giver 4, ikke 5.",
        (
            "// udfører heltalsdivision nedad; % giver resten.",
            "** repræsenterer potens; ^ er ikke potens.",
            "Præcedens kan ændres med parenteser.",
            "Enhver konvertering bør begrundes ud fra dataenes tilsigtede betydning.",
        ),
    ),
    (
        "Statements, input, output, and tracing",
        "A statement is an executable instruction. Assignment and a call to print() are examples. input() always returns a string, even when the user types digits; if a numeric quantity is required, conversion must be explicit. print() makes results visible, but printing is not the same as returning a value from a function. Tracing means following each statement, recording modified variables, and noting produced output.",
        (
            "input() always returns str.",
            "Visible output should match the specification.",
            "A correct trace follows the actual execution order.",
            "print() displays a value but does not change its type.",
        ),
        "Sætninger, input, output og gennemgang",
        "En sætning er en instruktion, der kan udføres. Tildeling og et kald til print() er eksempler. input() returnerer altid en tekststreng, også når brugeren skriver cifre; hvis der skal bruges en numerisk mængde, skal konverteringen være eksplicit. print() gør resultater synlige, men udskrivning er ikke det samme som at returnere en værdi fra en funktion. Gennemgang betyder at følge hver sætning, registrere ændrede variable og notere output.",
        (
            "input() returnerer altid str.",
            "Synligt output bør svare til specifikationen.",
            "En korrekt gennemgang følger den faktiske udførelsesrækkefølge.",
            "print() viser en værdi, men ændrer ikke dens type.",
        ),
    ),
    (
        "Errors, tests, and evidence of correctness",
        "A syntax error prevents Python from interpreting the code. A runtime error occurs while executing a syntactically valid statement, for example when dividing by zero or combining incompatible types. A logic error allows the program to finish but produces an incorrect result. The absence of exceptions does not prove correctness. A test compares an observed result with an expected result for a concrete input. Normal cases, boundaries, and cases that expose type or unit errors should be included.",
        (
            "Syntax, runtime, and logic describe different failures.",
            "An error message should be related to the operation that failed.",
            "A test needs an input, an expected result, and a comparison criterion.",
            "Several well-chosen cases provide more evidence than one execution.",
        ),
        "Fejl, test og evidens for korrekthed",
        "En syntaksfejl forhindrer Python i at fortolke koden. En kørselsfejl opstår under udførelsen af en syntaktisk gyldig sætning, for eksempel ved division med nul eller kombination af inkompatible typer. En logisk fejl lader programmet afslutte, men giver et forkert resultat. Fravær af undtagelser beviser ikke korrekthed. En test sammenligner et observeret resultat med et forventet resultat for et konkret input. Normale tilfælde, grænser og tilfælde, der afslører type- eller enhedsfejl, bør indgå.",
        (
            "Syntaks, kørsel og logik beskriver forskellige fejl.",
            "En fejlmeddelelse bør forbindes med den operation, der mislykkedes.",
            "En test kræver input, forventet resultat og et sammenligningskriterium.",
            "Flere velvalgte tilfælde giver mere evidens end én kørsel.",
        ),
    ),
)

_EXAMPLE_TRANSLATIONS = (
    (
        "Calculate the usable yield of a sequencing run",
        "A sequencing run produces 48_000_000 reads. A total of 92.5% pass quality control. Calculate the expected number of usable reads and display the result as an integer.",
        (
            "Represent the total as int and the percentage as float.",
            "Convert 92.5% to the fraction 0.925.",
            "Multiply the total by the fraction to obtain a float.",
            "Convert to int at the end because the result is a count.",
        ),
        "Underscores improve readability. Division produces 0.925 as float, and the final conversion to int is justified because the result is a count of reads.",
        "Beregn det anvendelige udbytte fra en sekventeringskørsel",
        "En sekventeringskørsel producerer 48_000_000 reads. I alt 92,5 % består kvalitetskontrollen. Beregn det forventede antal anvendelige reads og vis resultatet som et heltal.",
        (
            "Repræsenter totalen som int og procentdelen som float.",
            "Konvertér 92,5 % til brøken 0.925.",
            "Gang totalen med brøken for at få en float.",
            "Konvertér til int til sidst, fordi resultatet er et antal.",
        ),
        "Understregninger forbedrer læsbarheden. Divisionen giver 0.925 som float, og den afsluttende konvertering til int er begrundet, fordi resultatet er et antal reads.",
    ),
    (
        "Convert total volume between microlitres and millilitres",
        "Twenty-four samples are prepared and each requires 35 microlitres. Calculate the total volume in microlitres and millilitres.",
        (
            "Identify two integer inputs: sample count and volume per sample.",
            "Multiply to obtain the total in microlitres.",
            "Divide by 1000 to convert to millilitres.",
            "Keep units in variable names.",
        ),
        "The suffixes _ul and _ml make the unit explicit. Multiplication preserves int and division with / produces float. The result is consistent: 840 µL equals 0.84 mL.",
        "Konvertér samlet volumen mellem mikroliter og milliliter",
        "Der forberedes 24 prøver, og hver kræver 35 mikroliter. Beregn det samlede volumen i mikroliter og milliliter.",
        (
            "Identificér to heltalsinput: antal prøver og volumen pr. prøve.",
            "Gang for at få det samlede volumen i mikroliter.",
            "Divider med 1000 for at konvertere til milliliter.",
            "Behold enhederne i variabelnavnene.",
        ),
        "Endelserne _ul og _ml gør enheden tydelig. Multiplikation bevarer int, og division med / giver float. Resultatet er konsistent: 840 µL svarer til 0,84 mL.",
    ),
    (
        "Transform text input into a numeric count",
        "The user enters the sample count as text. The program must add two controls and display the total number of tubes required.",
        (
            "Recognise that input() returns str.",
            "Convert the string to int before adding.",
            "Keep the text representation and numeric quantity separate.",
        ),
        "Without int(), '18' + 2 raises TypeError because str and int cannot be added directly. Converting once and using a different name makes the change in representation explicit.",
        "Konvertér tekstinput til et numerisk antal",
        "Brugeren indtaster antallet af prøver som tekst. Programmet skal tilføje to kontroller og vise det samlede antal nødvendige rør.",
        (
            "Erkend, at input() returnerer str.",
            "Konvertér strengen til int før addition.",
            "Hold tekstrepræsentationen og den numeriske mængde adskilt.",
        ),
        "Uden int() giver '18' + 2 en TypeError, fordi str og int ikke kan lægges direkte sammen. En enkelt konvertering og et nyt navn gør ændringen i repræsentation tydelig.",
    ),
)

_PRACTICE_EN_DA = (
    (
        "Without running the code, determine the final value and type of a, b, and c:\na = 7\nb = a / 2\nc = a // 2",
        ("Compare / with //.", "Division with / produces float."),
        "a = 7 (int), b = 3.5 (float), c = 3 (int)",
        "a keeps the integer literal. / produces 3.5 and // produces 3.",
        "Uden at køre koden, bestem den endelige værdi og type for a, b og c:\na = 7\nb = a / 2\nc = a // 2",
        ("Sammenlign / med //.", "Division med / giver float."),
        "a = 7 (int), b = 3.5 (float), c = 3 (int)",
        "a bevarer heltalsliteralen. / giver 3.5, og // giver 3.",
    ),
    (
        "Match expression, value, type, variable, and assignment with their definitions.",
        ("Ask what is evaluated, what is obtained, and what changes state.",),
        "expression → evaluable code; value → result; type → category of operations; variable → name associated with a value; assignment → updates a name after evaluating the right-hand side",
        "The distinction allows precise descriptions of execution.",
        "Match udtryk, værdi, type, variabel og tildeling med deres definitioner.",
        ("Spørg, hvad der evalueres, hvad der opnås, og hvad der ændrer tilstanden.",),
        "udtryk → kode der kan evalueres; værdi → resultat; type → kategori af operationer; variabel → navn knyttet til en værdi; tildeling → opdaterer et navn efter evaluering af højresiden",
        "Skelnen gør det muligt at beskrive udførelsen præcist.",
    ),
    (
        "Build a trace table for:\ncount = 12\ncount = count + 3\ndouble_count = count * 2\ncount = 5",
        (
            "Record the state after each assignment.",
            "Reassigning count does not automatically change double_count.",
        ),
        "Line 1: count=12. Line 2: count=15. Line 3: count=15, double_count=30. Line 4: count=5, double_count=30.",
        "double_count keeps the value calculated on the third line.",
        "Lav en gennemgangstabel for:\ncount = 12\ncount = count + 3\ndouble_count = count * 2\ncount = 5",
        (
            "Registrér tilstanden efter hver tildeling.",
            "Gentildeling af count ændrer ikke automatisk double_count.",
        ),
        "Linje 1: count=12. Linje 2: count=15. Linje 3: count=15, double_count=30. Linje 4: count=5, double_count=30.",
        "double_count bevarer værdien beregnet på tredje linje.",
    ),
    (
        "Complete a program that converts 2.75 mL to microlitres and stores the result as an integer.",
        ("1 mL equals 1000 µL.", "Convert the unit before converting the type."),
        "volume_ul = int(volume_ml * 1000)",
        "Multiplication produces 2750.0 and int represents it as 2750.",
        "Fuldfør et program, der konverterer 2,75 mL til mikroliter og gemmer resultatet som et heltal.",
        ("1 mL svarer til 1000 µL.", "Konvertér enheden før typen."),
        "volume_ul = int(volume_ml * 1000)",
        "Multiplikationen giver 2750.0, og int repræsenterer det som 2750.",
    ),
    (
        "Correct the error and explain its cause:\nsample_count = '16'\ntotal = sample_count + 2\nprint(total)",
        (
            "Inspect the types of both operands of +.",
            "Decide whether concatenation or arithmetic addition is intended.",
        ),
        "sample_count = int('16')\ntotal = sample_count + 2\nprint(total)",
        "The original code combines str and int; the quantity should be converted to int.",
        "Ret fejlen og forklar årsagen:\nsample_count = '16'\ntotal = sample_count + 2\nprint(total)",
        (
            "Undersøg typerne for begge operander til +.",
            "Afgør, om der ønskes sammenkædning eller aritmetisk addition.",
        ),
        "sample_count = int('16')\ntotal = sample_count + 2\nprint(total)",
        "Den oprindelige kode kombinerer str og int; mængden bør konverteres til int.",
    ),
    (
        "Explain why (8 + 4) * 3 and 8 + 4 * 3 produce different results.",
        ("Describe precedence and the effect of parentheses.",),
        "Parentheses force addition first: 12 * 3 = 36. Without parentheses, multiplication occurs first: 8 + 12 = 20.",
        "The answer should justify the evaluation order.",
        "Forklar, hvorfor (8 + 4) * 3 og 8 + 4 * 3 giver forskellige resultater.",
        ("Beskriv præcedens og parentesernes virkning.",),
        "Parenteserne tvinger addition først: 12 * 3 = 36. Uden parenteser udføres multiplikationen først: 8 + 12 = 20.",
        "Svaret bør begrunde evalueringsrækkefølgen.",
    ),
    (
        "Complete: input() always returns a value of type ____; to use it as an integer, apply ____().",
        ("The first answer is the text type.",),
        "str; int",
        "input() produces text; int() converts a valid numeric string to an integer.",
        "Udfyld: input() returnerer altid en værdi af typen ____; for at bruge den som heltal kan man anvende ____().",
        ("Det første svar er teksttypen.",),
        "str; int",
        "input() producerer tekst; int() konverterer en gyldig numerisk streng til et heltal.",
    ),
    (
        "Explain orally the difference between a program that finishes without exceptions and a correct program. Include a logic error.",
        (
            "Define correctness relative to a specification.",
            "Use an example involving units or precedence.",
        ),
        "A program may finish and still violate the specification. Dividing microlitres by 100 instead of 1000 raises no exception but gives an incorrect conversion.",
        "A strong answer distinguishes execution from correctness.",
        "Forklar mundtligt forskellen mellem et program, der afslutter uden undtagelser, og et korrekt program. Medtag en logisk fejl.",
        (
            "Definér korrekthed i forhold til en specifikation.",
            "Brug et eksempel med enheder eller præcedens.",
        ),
        "Et program kan afslutte og stadig bryde specifikationen. At dividere mikroliter med 100 i stedet for 1000 giver ingen undtagelse, men en forkert konvertering.",
        "Et stærkt svar skelner mellem udførelse og korrekthed.",
    ),
)


def _localized_objectives() -> tuple[LocalizedLearningObjective, ...]:
    return tuple(
        LocalizedLearningObjective(
            objective_id=source.objective_id,
            statement=_t(source.statement, english, danish),
        )
        for source, english, danish in zip(
            _ES.objectives,
            _OBJECTIVES_EN,
            _OBJECTIVES_DA,
            strict=True,
        )
    )


def _localized_concepts() -> tuple[LocalizedConceptBlock, ...]:
    concepts: list[LocalizedConceptBlock] = []
    for source, translation in zip(_ES.concepts, _CONCEPT_TRANSLATIONS, strict=True):
        title_en, body_en, points_en, title_da, body_da, points_da = translation
        concepts.append(
            LocalizedConceptBlock(
                concept_id=source.concept_id,
                title=_t(source.title, title_en, title_da),
                body=_t(source.body, body_en, body_da),
                key_points=tuple(
                    _t(es, en, da)
                    for es, en, da in zip(
                        source.key_points,
                        points_en,
                        points_da,
                        strict=True,
                    )
                ),
            )
        )
    return tuple(concepts)


def _localized_examples() -> tuple[LocalizedWorkedExample, ...]:
    examples: list[LocalizedWorkedExample] = []
    for source, translation in zip(_ES.worked_examples, _EXAMPLE_TRANSLATIONS, strict=True):
        (
            title_en,
            problem_en,
            reasoning_en,
            explanation_en,
            title_da,
            problem_da,
            reasoning_da,
            explanation_da,
        ) = translation
        examples.append(
            LocalizedWorkedExample(
                example_id=source.example_id,
                title=_t(source.title, title_en, title_da),
                problem=_t(source.problem, problem_en, problem_da),
                reasoning=tuple(
                    _t(es, en, da)
                    for es, en, da in zip(
                        source.reasoning,
                        reasoning_en,
                        reasoning_da,
                        strict=True,
                    )
                ),
                code=_same(source.code),
                expected_output=_same(source.expected_output),
                explanation=_t(source.explanation, explanation_en, explanation_da),
            )
        )
    return tuple(examples)


def _localized_practice() -> tuple[LocalizedPracticeExercise, ...]:
    exercises: list[LocalizedPracticeExercise] = []
    for source, translation in zip(_ES.practice_exercises, _PRACTICE_EN_DA, strict=True):
        (
            prompt_en,
            hints_en,
            solution_en,
            explanation_en,
            prompt_da,
            hints_da,
            solution_da,
            explanation_da,
        ) = translation
        exercises.append(
            LocalizedPracticeExercise(
                exercise_id=source.exercise_id,
                activity_type=source.activity_type,
                prompt=_t(source.prompt, prompt_en, prompt_da),
                hints=tuple(
                    _t(es, en, da)
                    for es, en, da in zip(source.hints, hints_en, hints_da, strict=True)
                ),
                solution=_t(source.solution, solution_en, solution_da),
                explanation=_t(source.explanation, explanation_en, explanation_da),
                starter_code=_same(source.starter_code) if source.starter_code else None,
            )
        )
    return tuple(exercises)


def _localized_assessments() -> tuple[LocalizedAssessmentItem, ...]:
    source = _ES.assessment_items
    return (
        LocalizedAssessmentItem(
            item_id=source[0].item_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            prompt=_t(
                source[0].prompt,
                "Which statement best describes an expression in Python?",
                "Hvilken påstand beskriver bedst et udtryk i Python?",
            ),
            options=(
                _option(
                    "evaluates",
                    source[0].options[0],
                    "An evaluable combination that produces a value",
                    "En kombination, der kan evalueres og giver en værdi",
                ),
                _option(
                    "permanent",
                    source[0].options[1],
                    "A name permanently associated with a type",
                    "Et navn, der permanent er knyttet til en type",
                ),
                _option(
                    "prints",
                    source[0].options[2],
                    "Any line that prints text",
                    "Enhver linje, der udskriver tekst",
                ),
                _option(
                    "error",
                    source[0].options[3],
                    "An error detected at runtime",
                    "En fejl, der opdages under kørsel",
                ),
            ),
            correct_option_ids=("evaluates",),
            accepted_answers=(),
            explanation=_t(
                source[0].explanation,
                "An expression may contain literals, variables, operators, and calls, and produces a value when evaluated.",
                "Et udtryk kan indeholde literaler, variable, operatorer og kald og giver en værdi, når det evalueres.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[1].item_id,
            activity_type=ActivityType.TRUE_FALSE,
            prompt=_t(
                source[1].prompt,
                "The statement x = x + 1 expresses mathematical equality.",
                "Sætningen x = x + 1 udtrykker matematisk lighed.",
            ),
            options=(
                _option("true", "Verdadero", "True", "Sandt"),
                _option("false", "Falso", "False", "Falsk"),
            ),
            correct_option_ids=("false",),
            accepted_answers=(),
            explanation=_t(
                source[1].explanation,
                "It is a state update: x + 1 is evaluated and x is then reassigned.",
                "Det er en tilstandsopdatering: x + 1 evalueres, og derefter gentildeles x.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[2].item_id,
            activity_type=ActivityType.MULTIPLE_SELECT,
            prompt=_t(
                source[2].prompt,
                "Select all expressions whose result is a float.",
                "Vælg alle udtryk, hvis resultat er en float.",
            ),
            options=tuple(
                _option(option_id, es, es, es)
                for option_id, es in zip(
                    ("div", "floor", "float_cast", "add", "int_cast"),
                    source[2].options,
                    strict=True,
                )
            ),
            correct_option_ids=("div", "float_cast"),
            accepted_answers=(),
            explanation=_t(
                source[2].explanation,
                "/ produces float and float(5) creates 5.0; the others produce int.",
                "/ giver float, og float(5) opretter 5.0; de øvrige giver int.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[3].item_id,
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t(
                source[3].prompt,
                "Give the exact output:\nx = 4\ny = x + 3\nx = 10\nprint(y)",
                "Angiv det præcise output:\nx = 4\ny = x + 3\nx = 10\nprint(y)",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("7"),),
            explanation=_t(
                source[3].explanation,
                "y receives 7 before x is reassigned.",
                "y får værdien 7, før x gentildeles.",
            ),
            rubric=(
                _t(source[3].rubric[0], "States the output 7.", "Angiver outputtet 7."),
                _t(
                    source[3].rubric[1],
                    "Explains that variables do not retain an automatic dependency.",
                    "Forklarer, at variable ikke bevarer en automatisk afhængighed.",
                ),
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[4].item_id,
            activity_type=ActivityType.FILL_IN_THE_BLANK,
            prompt=_t(
                source[4].prompt,
                "The exponentiation operator in Python is ____.",
                "Potensoperatoren i Python er ____.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("**"),),
            explanation=_t(
                source[4].explanation,
                "Python uses **; ^ is a bitwise operation.",
                "Python bruger **; ^ er en bitvis operation.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[5].item_id,
            activity_type=ActivityType.DEBUGGING,
            prompt=_t(
                source[5].prompt,
                "Identify the main error in total = '12' / 3 and propose a correction.",
                "Identificér hovedfejlen i total = '12' / 3 og foreslå en rettelse.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(
                _t(
                    source[5].correct_answers[0],
                    "TypeError; total = int('12') / 3",
                    "TypeError; total = int('12') / 3",
                ),
            ),
            explanation=_t(
                source[5].explanation,
                "The syntax is valid, but / does not accept str as a numeric operand.",
                "Syntaksen er gyldig, men / accepterer ikke str som numerisk operand.",
            ),
            rubric=tuple(
                _t(es, en, da)
                for es, en, da in zip(
                    source[5].rubric,
                    (
                        "Identifies TypeError or a type mismatch.",
                        "Converts the string before division.",
                        "Justifies the conversion using the numeric meaning.",
                    ),
                    (
                        "Identificerer TypeError eller typeuoverensstemmelse.",
                        "Konverterer strengen før division.",
                        "Begrunder konverteringen ud fra den numeriske betydning.",
                    ),
                    strict=True,
                )
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[6].item_id,
            activity_type=ActivityType.ORDERING,
            prompt=_t(
                source[6].prompt,
                "Order the stages from the real situation to concrete execution.",
                "Sæt faserne i rækkefølge fra den virkelige situation til konkret udførelse.",
            ),
            options=(
                _option("program", "Programa", "Program", "Program"),
                _option("problem", "Problema", "Problem", "Problem"),
                _option("algorithm", "Algoritmo", "Algorithm", "Algoritme"),
                _option("model", "Modelo", "Model", "Model"),
            ),
            correct_option_ids=("problem", "model", "algorithm", "program"),
            accepted_answers=(),
            explanation=_t(
                source[6].explanation,
                "Problem, model, algorithm, and program form the correct sequence.",
                "Problem, model, algoritme og program er den korrekte rækkefølge.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[7].item_id,
            activity_type=ActivityType.MATCHING,
            prompt=_t(
                source[7].prompt,
                "Match each error with its description.",
                "Match hver fejl med dens beskrivelse.",
            ),
            options=(
                _option(
                    "syntax",
                    source[7].options[0],
                    "SyntaxError → invalid structure",
                    "SyntaxError → ugyldig struktur",
                ),
                _option(
                    "type",
                    source[7].options[1],
                    "TypeError → operation incompatible with the types",
                    "TypeError → operation uforenelig med typerne",
                ),
                _option(
                    "logic",
                    source[7].options[2],
                    "Logic error → incorrect result without necessarily raising an exception",
                    "Logisk fejl → forkert resultat uden nødvendigvis at udløse en undtagelse",
                ),
            ),
            correct_option_ids=("syntax", "type", "logic"),
            accepted_answers=(),
            explanation=_t(
                source[7].explanation,
                "The three categories require different diagnostic strategies.",
                "De tre kategorier kræver forskellige diagnostiske strategier.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[8].item_id,
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t(
                source[8].prompt,
                "Define the minimum information a program test must contain.",
                "Definér den minimale information, som en programtest skal indeholde.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(
                _t(
                    source[8].correct_answers[0],
                    "A concrete input, an expected result, and a comparison criterion.",
                    "Et konkret input, et forventet resultat og et sammenligningskriterium.",
                ),
            ),
            explanation=_t(
                source[8].explanation,
                "Without an expected result there is no test, only execution.",
                "Uden et forventet resultat er der ingen test, kun udførelse.",
            ),
            rubric=tuple(
                _t(es, en, da)
                for es, en, da in zip(
                    source[8].rubric,
                    (
                        "Mentions the input.",
                        "Mentions the expected result.",
                        "Mentions comparison or an acceptance criterion.",
                    ),
                    (
                        "Nævner inputtet.",
                        "Nævner det forventede resultat.",
                        "Nævner sammenligning eller acceptkriterium.",
                    ),
                    strict=True,
                )
            ),
        ),
        LocalizedAssessmentItem(
            item_id=source[9].item_id,
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=_t(
                source[9].prompt,
                "Complete so the output is 1500:\nvolume_ml = 1.5\nvolume_ul = ____\nprint(volume_ul)",
                "Udfyld, så outputtet bliver 1500:\nvolume_ml = 1.5\nvolume_ul = ____\nprint(volume_ul)",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("int(volume_ml * 1000)"),),
            explanation=_t(
                source[9].explanation,
                "Multiplying by 1000 converts mL to µL and int represents the count without a fractional part.",
                "Multiplikation med 1000 konverterer mL til µL, og int repræsenterer antallet uden decimaldel.",
            ),
        ),
    )


def _localized_tutor_support() -> LocalizedTutorSupportPacket:
    source = _ES.tutor_support
    canonical_en = (
        "This module teaches how to interpret a program as a verifiable transformation from inputs to outputs. "
        "The learner separates the concrete problem, the model that retains relevant variables, the algorithm "
        "that specifies the steps, and the Python program that executes them. Within the program, an expression "
        "is evaluated to produce a value; each value has a type; a variable is a name associated with its current "
        "value; and an assignment changes state after fully evaluating its right-hand side. Understanding is shown "
        "by predicting results, tracing state, and justifying conversions from data meaning rather than memorising "
        "symbols. Correctness requires comparing observed behaviour with a specification through tests that define "
        "an input, an expected result, and an acceptance criterion."
    )
    canonical_da = (
        "Dette modul lærer den studerende at fortolke et program som en efterprøvelig transformation fra input "
        "til output. Den studerende adskiller det konkrete problem, modellen der bevarer relevante variable, "
        "algoritmen der beskriver trinene, og Python-programmet der udfører dem. I programmet evalueres et udtryk "
        "for at give en værdi; hver værdi har en type; en variabel er et navn knyttet til den aktuelle værdi; og "
        "en tildeling ændrer tilstanden efter fuld evaluering af højresiden. Forståelse vises ved at forudsige "
        "resultater, følge tilstanden og begrunde konverteringer ud fra dataenes betydning frem for at huske "
        "symboler. Korrekthed kræver sammenligning af observeret adfærd med en specifikation gennem test, der "
        "definerer input, forventet resultat og acceptkriterium."
    )
    knowledge_en = (
        "/ produces float and // produces the floor quotient.",
        "input() returns str; a numeric string must be converted before arithmetic.",
        "A variable may be reassigned, but every value has a defined type.",
        "Assignment evaluates the right-hand side first and then updates the left-hand name.",
        "Reassigning a variable does not automatically recalculate other variables.",
        "int() applied to float removes the fractional part toward zero.",
        "Parentheses may change precedence and document intent.",
        "A program without exceptions may still contain a logic error.",
        "A test needs an expected result defined in advance.",
        "Names containing units reduce dimensional errors.",
    )
    knowledge_da = (
        "/ giver float, og // giver heltalskvotienten nedad.",
        "input() returnerer str; en numerisk streng skal konverteres før aritmetik.",
        "En variabel kan gentildeles, men hver værdi har en bestemt type.",
        "Tildeling evaluerer først højresiden og opdaterer derefter navnet til venstre.",
        "Gentildeling af en variabel genberegner ikke automatisk andre variable.",
        "int() anvendt på float fjerner decimaldelen mod nul.",
        "Parenteser kan ændre præcedens og dokumentere hensigten.",
        "Et program uden undtagelser kan stadig indeholde en logisk fejl.",
        "En test kræver et forventet resultat, der er defineret på forhånd.",
        "Navne med enheder reducerer dimensionsfejl.",
    )
    misconceptions_en = (
        "Confusing = with mathematical equality.",
        "Believing that '12' is a number because it contains digits.",
        "Assuming int(4.9) rounds to 5.",
        "Using ^ for exponentiation.",
        "Thinking that changing x automatically updates y.",
        "Treating every error as a syntax error.",
        "Considering exception-free completion proof of correctness.",
        "Omitting units from numeric variables.",
    )
    misconceptions_da = (
        "At forveksle = med matematisk lighed.",
        "At tro, at '12' er et tal, fordi det indeholder cifre.",
        "At antage, at int(4.9) afrunder til 5.",
        "At bruge ^ som potensoperator.",
        "At tro, at en ændring af x automatisk opdaterer y.",
        "At fortolke enhver fejl som en syntaksfejl.",
        "At betragte afslutning uden undtagelser som bevis for korrekthed.",
        "At udelade enheder fra numeriske variable.",
    )
    questions_en = (
        "What are the inputs and what type should each have?",
        "What value does the right-hand expression produce first?",
        "Which names change after this statement?",
        "Is the operation defined for those types?",
        "What unit does each variable represent?",
        "What result do you expect for a small input?",
        "Does the failure prevent execution or produce a wrong answer?",
        "Can you build one trace row per statement?",
    )
    questions_da = (
        "Hvad er inputtene, og hvilken type bør hvert input have?",
        "Hvilken værdi giver udtrykket til højre først?",
        "Hvilke navne ændres efter denne sætning?",
        "Er operationen defineret for disse typer?",
        "Hvilken enhed repræsenterer hver variabel?",
        "Hvilket resultat forventer du for et lille input?",
        "Forhindrer fejlen udførelse, eller giver den et forkert svar?",
        "Kan du oprette én gennemgangsrække pr. sætning?",
    )
    criteria_en = (
        "Uses technical vocabulary correctly.",
        "Predicts both value and type when required.",
        "Justifies conversions.",
        "Maintains unit consistency.",
        "Explains evaluation order.",
        "Distinguishes syntax, runtime, and logic.",
        "Proposes concrete tests.",
        "Connects code with the specification.",
    )
    criteria_da = (
        "Bruger teknisk ordforråd korrekt.",
        "Forudsiger både værdi og type, når det kræves.",
        "Begrunder konverteringer.",
        "Bevarer konsistens i enheder.",
        "Forklarer evalueringsrækkefølgen.",
        "Skelner mellem syntaks, kørsel og logik.",
        "Foreslår konkrete test.",
        "Forbinder koden med specifikationen.",
    )
    constraints_en = (
        "Give a hint first during an exercise unless the full solution is explicitly requested.",
        "Do not invent Python rules; propose a minimal test when uncertain.",
        "Do not validate a result without checking reasoning and types.",
        "Do not introduce conditionals, loops, advanced functions, or objects when only this module's concepts are required.",
        "Separate conceptual explanation, tracing, and corrected code.",
        "Point out unit errors before secondary syntax details.",
        "Use biomedical examples as context, not as clinical advice.",
    )
    constraints_da = (
        "Giv først et hint under en øvelse, medmindre den fulde løsning udtrykkeligt ønskes.",
        "Opfind ikke Python-regler; foreslå en minimal test ved tvivl.",
        "Godkend ikke et resultat uden at kontrollere ræsonnement og typer.",
        "Introducér ikke betingelser, løkker, avancerede funktioner eller objekter, når kun modulets begreber kræves.",
        "Adskil konceptuel forklaring, gennemgang og rettet kode.",
        "Påpeg enhedsfejl før sekundære syntaksdetaljer.",
        "Brug biomedicinske eksempler som kontekst, ikke som klinisk rådgivning.",
    )
    return LocalizedTutorSupportPacket(
        canonical_explanation=_t(source.canonical_explanation, canonical_en, canonical_da),
        knowledge_fragments=tuple(
            _t(es, en, da)
            for es, en, da in zip(
                source.knowledge_fragments, knowledge_en, knowledge_da, strict=True
            )
        ),
        common_misconceptions=tuple(
            _t(es, en, da)
            for es, en, da in zip(
                source.common_misconceptions, misconceptions_en, misconceptions_da, strict=True
            )
        ),
        socratic_questions=tuple(
            _t(es, en, da)
            for es, en, da in zip(
                source.socratic_questions, questions_en, questions_da, strict=True
            )
        ),
        grading_criteria=tuple(
            _t(es, en, da)
            for es, en, da in zip(source.grading_criteria, criteria_en, criteria_da, strict=True)
        ),
        response_constraints=tuple(
            _t(es, en, da)
            for es, en, da in zip(
                source.response_constraints, constraints_en, constraints_da, strict=True
            )
        ),
        source_basis=source.source_basis,
    )


LOCALIZED_MODULE = LocalizedLearningModule(
    course_code=_ES.course_code,
    module_id=_ES.module_id,
    title=_t(
        _ES.title,
        "Problem solving, values, types, and program state",
        "Problemløsning, værdier, typer og programtilstand",
    ),
    summary=_t(
        _ES.summary,
        "An introduction to computational reasoning and the minimum elements of a Python program: problem, model, algorithm, expressions, values, types, variables, assignment, type conversion, input and output, tracing, errors, and basic testing.",
        "En introduktion til computationel tænkning og de grundlæggende elementer i et Python-program: problem, model, algoritme, udtryk, værdier, typer, variable, tildeling, typekonvertering, input og output, gennemgang, fejl og grundlæggende test.",
    ),
    objectives=_localized_objectives(),
    concepts=_localized_concepts(),
    worked_examples=_localized_examples(),
    practice_exercises=_localized_practice(),
    assessment_items=_localized_assessments(),
    tutor_support=_localized_tutor_support(),
)

__all__ = ["LOCALIZED_MODULE"]
