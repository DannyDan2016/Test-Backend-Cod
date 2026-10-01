"""Traducción de los tags Gherkin a marcadores de pytest compatibles con ``--strict-markers``.

pytest-bdd convierte cada tag en un marcador con el mismo nombre. Con ``--strict-markers`` eso
obligaría a registrar cada ``@tc-api-NNN``, así que este módulo intercepta los tags especiales:

- ``@tc-<area>-NNN`` -> marcador ``tc("TC-<AREA>-NNN")`` + etiquetas Allure ``ID`` y ``tag``.
- ``@known-bug``     -> marcador ``known_bug`` (se convierte en ``xfail(strict=True)``).
- ``@bug:<ID>``      -> marcador ``bug("<ID>")``; el motivo del xfail se lee del catálogo
  ``bugs_conocidos`` de los datos YAML.

El resto de tags (``@smoke``, ``@regression``...) siguen el comportamiento por defecto y deben
estar registrados en ``pytest.ini``.

Limitación de pytest-bdd 9: los tags de un bloque ``Ejemplos`` no pasan por el hook
``pytest_bdd_apply_tag``, así que ahí solo se pueden usar marcadores registrados.
"""

import re
from collections.abc import Callable, Iterable
from typing import Any

import pytest

from support.data_loader import DataKeyError, TestData

TAG_TC = re.compile(r"^tc-[a-z]+-\d{3}$")
TAG_BUG = re.compile(r"^bug:(?P<id>[A-Za-z0-9-]+)$")
TAG_KNOWN_BUG = "known-bug"
CATALOGO_BUGS = "bugs_conocidos"


def apply_tag(tag: str, function: Callable[..., Any]) -> bool | None:
    """Aplica los tags especiales; devuelve ``True`` si el tag queda gestionado."""
    if TAG_TC.match(tag):
        tc_id = tag.upper()
        pytest.mark.tc(tc_id)(function)
        pytest.mark.allure_label(tc_id, label_type="as_id")(function)
        pytest.mark.allure_label(tc_id, label_type="tag")(function)
        return True
    if tag == TAG_KNOWN_BUG:
        pytest.mark.known_bug(function)
        return True
    if match := TAG_BUG.match(tag):
        pytest.mark.bug(match["id"])(function)
        return True
    return None


def tc_ids(item: pytest.Item) -> list[str]:
    """IDs de caso de prueba (``TC-...``) asociados al escenario."""
    return [marca.args[0] for marca in item.iter_markers("tc")]


def mark_known_bugs(items: Iterable[pytest.Item], env: str) -> None:
    """Convierte ``@known-bug`` en ``xfail(strict=True)`` con el motivo del catálogo de bugs.

    El escenario verifica el comportamiento CORRECTO: falla mientras el bug exista y, con
    ``strict=True``, el día que se corrija el XPASS rompe la ejecución para revisar el caso.
    """
    con_bug = [item for item in items if item.get_closest_marker("known_bug") is not None]
    if not con_bug:
        return
    test_data = TestData(env)
    for item in con_bug:
        bugs = [marca.args[0] for marca in item.iter_markers("bug")]
        if not bugs:
            raise pytest.UsageError(f"{item.nodeid}: @known-bug necesita un tag @bug:<ID>")
        motivos = []
        for bug_id in bugs:
            try:
                resumen = test_data.get(f"{CATALOGO_BUGS}.{bug_id}.resumen")
            except DataKeyError as error:
                raise pytest.UsageError(f"{item.nodeid}: {error}") from error
            motivos.append(f"{bug_id}: {resumen}")
        item.add_marker(pytest.mark.xfail(strict=True, reason=" | ".join(motivos)))
