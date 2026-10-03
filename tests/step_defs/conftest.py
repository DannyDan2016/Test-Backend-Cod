"""Pasos y fixtures comunes a todas las features.

Los pasos son delgados: cargan un caso del YAML, delegan la llamada en un service object y
verifican con ``assert_expected``. No contienen URLs ni valores de negocio.
"""

import pytest
from pytest_bdd import given, parsers, then

from support.assertions import assert_expected
from support.bdd_tags import tc_ids
from support.context import ScenarioContext
from support.data_loader import TestData


@pytest.fixture
def ctx() -> ScenarioContext:
    """Contexto nuevo por escenario."""
    return ScenarioContext()


@given(parsers.parse('el caso de prueba "{clave}"'))
def load_case(
    clave: str, test_data: TestData, ctx: ScenarioContext, request: pytest.FixtureRequest
):
    """Carga el caso del YAML y comprueba que su ``id`` coincide con un @tc-* del escenario."""
    caso = test_data.case(clave)
    ids_escenario = tc_ids(request.node)
    if caso.id and ids_escenario and caso.id not in ids_escenario:
        pytest.fail(
            f"El caso {clave!r} tiene id {caso.id} pero el escenario está etiquetado con "
            f"{ids_escenario}: revisa el tag @tc-* o el YAML"
        )
    ctx.case = caso


@then("la respuesta cumple lo esperado del caso")
def response_matches_case(ctx: ScenarioContext):
    caso = ctx.require_case()
    assert_expected(ctx.require_response(), caso.expected, sent_body=ctx.sent_body)
