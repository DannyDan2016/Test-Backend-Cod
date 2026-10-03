"""Pruebas unitarias del helper de aserción declarativa (sin red)."""

import json
from datetime import timedelta
from typing import Any

import pytest
import requests

from support.assertions import assert_expected

pytestmark = pytest.mark.unit


def _respuesta(
    status: int = 200,
    body: Any = None,
    headers: dict[str, str] | None = None,
    ms: int = 100,
    crudo: bytes | None = None,
) -> requests.Response:
    """Construye una ``Response`` a mano, como la devolvería requests."""
    resp = requests.Response()
    resp.status_code = status
    resp._content = crudo if crudo is not None else json.dumps(body).encode()
    resp.headers.update(headers or {"Content-Type": "application/json; charset=utf-8"})
    resp.elapsed = timedelta(milliseconds=ms)
    resp.url = "https://api.example.test/users"
    resp.request = requests.Request("POST", resp.url).prepare()
    return resp


CUERPO = {"name": "Ana", "age": 33, "id": "123", "data": [{"id": 1}, {"id": 2}]}


def test_pasa_cuando_todo_coincide():
    assert_expected(
        _respuesta(201, CUERPO),
        {
            "status": [200, 201],
            "max_time_ms": 500,
            "headers": {"Content-Type": "^application/json"},
            "json_equals": {"data.1.id": 2},
            "json_matches": {"id": r"^\d+$"},
            "json_types": {"age": "integer", "data": "array"},
            "json_length": {"data": 2},
            "json_absent": ["updatedAt"],
            "echo_body": True,
        },
        sent_body={"name": "Ana", "age": 33},
    )


def test_acumula_todos_los_fallos_en_un_solo_error():
    with pytest.raises(AssertionError) as error:
        assert_expected(
            _respuesta(400, CUERPO, ms=900),
            {
                "status": 201,
                "max_time_ms": 500,
                "json_equals": {"name": "Eva"},
                "json_absent": ["id"],
            },
        )

    mensaje = str(error.value)
    assert "POST https://api.example.test/users -> 400" in mensaje
    assert "status: esperado 201, obtenido 400" in mensaje
    assert "tiempo: 900 ms > máximo 500 ms" in mensaje
    assert "name: esperado 'Eva', obtenido 'Ana'" in mensaje
    assert "id: no debería estar presente" in mensaje


def test_el_eco_compara_tambien_el_tipo():
    with pytest.raises(AssertionError, match="eco age: enviado 33, devuelto '33'"):
        assert_expected(_respuesta(201, {"age": "33"}), {"echo_body": True}, sent_body={"age": 33})


def test_bool_no_cuenta_como_entero():
    with pytest.raises(AssertionError, match="se esperaba tipo integer"):
        assert_expected(_respuesta(body={"age": True}), {"json_types": {"age": "integer"}})


def test_ruta_inexistente_se_muestra_como_falta():
    with pytest.raises(AssertionError, match=r"data\.5\.id: esperado 1, obtenido <falta>"):
        assert_expected(_respuesta(body=CUERPO), {"json_equals": {"data.5.id": 1}})


def test_cuerpo_vacio():
    assert_expected(_respuesta(204, crudo=b"", headers={}), {"status": 204, "body_empty": True})
    with pytest.raises(AssertionError, match="se esperaba cuerpo vacío"):
        assert_expected(_respuesta(200, {"a": 1}), {"body_empty": True})


def test_respuesta_que_no_es_json():
    with pytest.raises(AssertionError, match="la respuesta no es JSON"):
        assert_expected(_respuesta(crudo=b"Not Found"), {"json_equals": {"a": 1}})


def test_solo_status_no_exige_cuerpo_json():
    assert_expected(_respuesta(404, crudo=b"Not Found"), {"status": 404})


def test_clave_desconocida_en_expected_es_un_error_de_datos():
    with pytest.raises(ValueError, match=r"no permitidas en expected: \['json_equal'\]"):
        assert_expected(_respuesta(body=CUERPO), {"json_equal": {"name": "Ana"}})
