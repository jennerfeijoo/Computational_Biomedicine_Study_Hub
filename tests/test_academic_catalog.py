from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.academic_catalog import AcademicCatalog


def test_catalog_exposes_all_dm857_modules_without_widgets() -> None:
    catalog = AcademicCatalog(locale=AppLocale.ENGLISH)

    modules = catalog.modules("DM857")
    cards = catalog.flashcards(course_code="DM857")
    glossary = catalog.glossary(course_code="DM857")

    assert len(modules) == 14
    assert modules[0].module_id == "dm857.m01"
    assert modules[-1].module_id == "dm857.m14"
    assert len(cards) > len(glossary) > 14
    assert len({card.card_id for card in cards}) == len(cards)
    assert len({entry.term_id for entry in glossary}) == len(glossary)
    assert all(entry.course_code == "DM857" for entry in glossary)


def test_catalog_keeps_identities_stable_while_materializing_other_languages() -> None:
    spanish = AcademicCatalog(locale=AppLocale.SPANISH_SPAIN)
    english = AcademicCatalog(locale=AppLocale.ENGLISH)
    danish = AcademicCatalog(locale=AppLocale.DANISH_DENMARK)

    assert tuple(module.module_id for module in spanish.modules()) == tuple(
        module.module_id for module in english.modules()
    )
    assert {entry.term_id for entry in spanish.glossary()} == {
        entry.term_id for entry in danish.glossary()
    }
    assert spanish.modules()[0].title != english.modules()[0].title
    assert spanish.glossary()[0].locale is AppLocale.SPANISH_SPAIN
    assert danish.glossary()[0].locale is AppLocale.DANISH_DENMARK


def test_empty_catalog_reports_no_academic_courses() -> None:
    catalog = AcademicCatalog(bundle_catalogs=())

    assert catalog.course_codes == ()
    assert catalog.modules() == ()
    assert catalog.flashcards() == ()
    assert catalog.glossary() == ()
