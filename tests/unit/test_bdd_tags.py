"""Pruebas unitarias de la traducción de tags Gherkin a marcadores (sin red)."""

import pytest

from support.bdd_tags import apply_tag

pytestmark = pytest.mark.unit


def _escenario():
    """Función nueva y vacía que hace de escenario de pytest-bdd."""

    def escenario():
        pass

    return escenario


def _marcas(funcion) -> list[tuple[str, tuple, dict]]:
    return [(m.name, m.args, m.kwargs) for m in getattr(funcion, "pytestmark", [])]


def test_tag_tc_se_convierte_en_marcador_y_etiquetas_allure():
    funcion = _escenario()

    assert apply_tag("tc-api-045", funcion) is True
    assert _marcas(funcion) == [
        ("tc", ("TC-API-045",), {}),
        ("allure_label", ("TC-API-045",), {"label_type": "as_id"}),
        ("allure_label", ("TC-API-045",), {"label_type": "tag"}),
    ]


def test_known_bug_y_bug_se_traducen_a_marcadores_registrados():
    funcion = _escenario()

    assert apply_tag("known-bug", funcion) is True
    assert apply_tag("bug:DEV-004", funcion) is True
    assert _marcas(funcion) == [("known_bug", (), {}), ("bug", ("DEV-004",), {})]


@pytest.mark.parametrize("tag", ["smoke", "regression", "tc-api-45", "tc-API-045", "bug:"])
def test_otros_tags_siguen_el_comportamiento_por_defecto(tag: str):
    assert apply_tag(tag, _escenario()) is None
