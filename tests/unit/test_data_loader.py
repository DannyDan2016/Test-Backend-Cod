"""Pruebas unitarias del cargador de datos YAML (sin red)."""

from pathlib import Path

import pytest

from support.data_loader import ClaveNoEncontradaError, DatosError, TestData, deep_merge

pytestmark = pytest.mark.unit


def _escribir(base: Path, relativa: str, contenido: str) -> None:
    ruta = base / relativa
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")


@pytest.fixture
def datos(tmp_path: Path) -> Path:
    base = tmp_path / "data"
    _escribir(
        base,
        "comun/api/usuarios.yaml",
        """
crear:
  id: TC-API-001
  descripcion: Crear usuario
  request:
    body: {name: Ana, job: QA}
  expected:
    status: 201
    max_time_ms: 2000
    json_absent: [updatedAt]
""",
    )
    _escribir(
        base,
        "staging/api/usuarios.yaml",
        """
crear:
  expected:
    max_time_ms: 5000
    json_absent: [deletedAt]
""",
    )
    return base


def test_deep_merge_el_override_gana_y_conserva_el_resto():
    base = {"a": 1, "b": {"c": 2, "d": 3}, "lista": [1, 2]}
    override = {"b": {"c": 20}, "lista": [9], "e": 5}

    assert deep_merge(base, override) == {"a": 1, "b": {"c": 20, "d": 3}, "lista": [9], "e": 5}


def test_sin_override_se_usan_los_datos_comunes(datos: Path):
    caso = TestData("prod", base_dir=datos).case("api.usuarios.crear")

    assert caso.id == "TC-API-001"
    assert caso.body == {"name": "Ana", "job": "QA"}
    assert caso.expected["max_time_ms"] == 2000


def test_el_ambiente_sobrescribe_en_profundidad(datos: Path):
    caso = TestData("staging", base_dir=datos).case("api.usuarios.crear")

    assert caso.expected["status"] == 201
    assert caso.expected["max_time_ms"] == 5000
    assert caso.expected["json_absent"] == ["deletedAt"]


def test_clave_inexistente_indica_tramo_archivo_y_disponibles(datos: Path):
    with pytest.raises(ClaveNoEncontradaError) as error:
        TestData("staging", base_dir=datos).get("api.usuarios.crearx")

    mensaje = str(error.value)
    assert "'crearx'" in mensaje
    assert "'api.usuarios'" in mensaje
    assert "data/comun/api/usuarios.yaml" in mensaje
    assert "data/staging/api/usuarios.yaml" in mensaje
    assert "Claves disponibles: crear" in mensaje


def test_caso_con_clave_mal_escrita_falla_de_forma_explicita(datos: Path):
    _escribir(datos, "comun/api/errata.yaml", "caso:\n  expectd: {status: 200}\n")

    with pytest.raises(DatosError, match=r"claves no permitidas: \['expectd'\]"):
        TestData("prod", base_dir=datos).case("api.errata.caso")


def test_yaml_invalido_indica_el_archivo(datos: Path):
    _escribir(datos, "comun/api/roto.yaml", "clave: [sin cerrar\n")

    with pytest.raises(DatosError, match=r"YAML inválido en .*roto\.yaml"):
        TestData("prod", base_dir=datos)
