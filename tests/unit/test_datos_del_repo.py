"""Validación estática de los datos YAML y contratos versionados (sin red).

Detecta erratas antes de ejecutar contra las APIs: claves no permitidas, contratos inexistentes
o mal escritos y casos cuyo override de ambiente rompe la estructura.
"""

from collections.abc import Iterator
from typing import Any

import pytest

from config.settings import AMBIENTES
from support.assertions import CLAVES_EXPECTED
from support.data_loader import TestData
from support.schemas import DIRECTORIO_SCHEMAS, load_validator

pytestmark = pytest.mark.unit


def _claves_de_casos(nodo: Any, prefijo: str = "") -> Iterator[str]:
    """Recorre los datos y devuelve la ruta de cada nodo que es un caso (tiene expected)."""
    if not isinstance(nodo, dict):
        return
    if "expected" in nodo:
        yield prefijo
        return
    for clave, valor in nodo.items():
        yield from _claves_de_casos(valor, f"{prefijo}.{clave}" if prefijo else clave)


@pytest.mark.parametrize("env", sorted(AMBIENTES))
def test_todos_los_casos_son_validos_en_cada_ambiente(env: str):
    datos = TestData(env)
    claves = list(_claves_de_casos(datos.get_all()))

    assert claves, f"No se encontró ningún caso en data/ para {env}"
    for clave in claves:
        caso = datos.case(clave)
        desconocidas = set(caso.expected) - CLAVES_EXPECTED
        assert not desconocidas, f"{clave}: claves no permitidas en expected {desconocidas}"
        if schema := caso.expected.get("schema"):
            load_validator(schema)


@pytest.mark.parametrize(
    "ruta", sorted(DIRECTORIO_SCHEMAS.rglob("*.schema.json")), ids=lambda ruta: ruta.stem
)
def test_todos_los_contratos_son_json_schema_validos(ruta):
    nombre = ruta.relative_to(DIRECTORIO_SCHEMAS).as_posix().removesuffix(".schema.json")
    load_validator(nombre)
