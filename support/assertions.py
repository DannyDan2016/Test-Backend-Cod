"""Aserción declarativa: compara una ``Response`` con el bloque ``expected`` de un caso YAML.

Acumula todos los fallos (soft assert) y los lanza juntos, para que un fallo de status no oculte
el resto de diferencias. Las claves admitidas en ``expected`` son:

- ``status``: código esperado (entero) o lista de códigos aceptados.
- ``max_time_ms`` / ``min_time_ms``: límites del tiempo de respuesta.
- ``headers``: ``{cabecera: regex}``.
- ``body_empty``: ``true`` si la respuesta no debe tener cuerpo.
- ``body_json``: cuerpo JSON exacto.
- ``schema``: nombre del contrato en ``schemas/`` (sin ``.schema.json``).
- ``json_equals``: ``{ruta: valor}``; la ruta admite puntos e índices (``data.0.id``).
- ``json_matches``: ``{ruta: regex}``.
- ``json_types``: ``{ruta: tipo}`` (string, integer, number, boolean, object, array, null).
- ``json_length``: ``{ruta: n}``.
- ``json_absent``: lista de rutas que no deben existir.
- ``echo_body``: ``true`` si la respuesta debe devolver cada campo enviado con el mismo valor.
"""

import re
from typing import Any

import requests

from support.schemas import schema_errors

CLAVES_EXPECTED = frozenset(
    {
        "status",
        "max_time_ms",
        "min_time_ms",
        "headers",
        "body_empty",
        "body_json",
        "schema",
        "json_equals",
        "json_matches",
        "json_types",
        "json_length",
        "json_absent",
        "echo_body",
    }
)

# Claves que necesitan leer el cuerpo como JSON
CLAVES_CUERPO = CLAVES_EXPECTED - {"status", "max_time_ms", "min_time_ms", "headers", "body_empty"}

TIPOS_JSON: dict[str, tuple[type, ...]] = {
    "string": (str,),
    "integer": (int,),
    "number": (int, float),
    "boolean": (bool,),
    "object": (dict,),
    "array": (list,),
    "null": (type(None),),
}

_FALTA = object()


def get_path(body: Any, ruta: str) -> Any:
    """Resuelve rutas con puntos e índices (``data.0.email``); devuelve ``_FALTA`` si no existe."""
    actual = body
    for parte in ruta.split("."):
        if isinstance(actual, list) and parte.isdigit() and int(parte) < len(actual):
            actual = actual[int(parte)]
        elif isinstance(actual, dict) and parte in actual:
            actual = actual[parte]
        else:
            return _FALTA
    return actual


def _mostrar(valor: Any) -> str:
    return "<falta>" if valor is _FALTA else repr(valor)


def _es_tipo(valor: Any, tipo: str) -> bool:
    # bool es subclase de int en Python, pero en JSON no es un número
    if tipo in ("integer", "number") and isinstance(valor, bool):
        return False
    return isinstance(valor, TIPOS_JSON[tipo])


def _validar_expected(expected: dict[str, Any]) -> None:
    if desconocidas := set(expected) - CLAVES_EXPECTED:
        raise ValueError(
            f"Claves no permitidas en expected: {sorted(desconocidas)}. "
            f"Permitidas: {sorted(CLAVES_EXPECTED)}"
        )
    for ruta, tipo in (expected.get("json_types") or {}).items():
        if tipo not in TIPOS_JSON:
            raise ValueError(f"json_types.{ruta}: tipo desconocido {tipo!r}")


def _errores_cuerpo(body: Any, expected: dict[str, Any], sent_body: Any) -> list[str]:
    errores: list[str] = []
    if "body_json" in expected and body != expected["body_json"]:
        errores.append(f"cuerpo: esperado {expected['body_json']!r}, obtenido {body!r}")

    if schema := expected.get("schema"):
        errores += schema_errors(schema, body)

    for ruta, valor in (expected.get("json_equals") or {}).items():
        real = get_path(body, ruta)
        if real is _FALTA or real != valor:
            errores.append(f"{ruta}: esperado {valor!r}, obtenido {_mostrar(real)}")

    for ruta, patron in (expected.get("json_matches") or {}).items():
        real = get_path(body, ruta)
        if real is _FALTA or not re.search(patron, str(real)):
            errores.append(f"{ruta}: {_mostrar(real)} no cumple /{patron}/")

    for ruta, tipo in (expected.get("json_types") or {}).items():
        real = get_path(body, ruta)
        if real is _FALTA or not _es_tipo(real, tipo):
            errores.append(f"{ruta}: se esperaba tipo {tipo}, obtenido {_mostrar(real)}")

    for ruta, n in (expected.get("json_length") or {}).items():
        real = get_path(body, ruta)
        if real is _FALTA or not hasattr(real, "__len__") or len(real) != n:
            longitud = (
                "<falta>" if real is _FALTA else len(real) if hasattr(real, "__len__") else "-"
            )
            errores.append(f"len({ruta}): esperado {n}, obtenido {longitud}")

    for ruta in expected.get("json_absent") or []:
        if get_path(body, ruta) is not _FALTA:
            errores.append(f"{ruta}: no debería estar presente")

    if expected.get("echo_body") and isinstance(sent_body, dict):
        for clave, valor in sent_body.items():
            real = get_path(body, clave) if isinstance(body, dict) else _FALTA
            if real is _FALTA or real != valor or type(real) is not type(valor):
                errores.append(f"eco {clave}: enviado {valor!r}, devuelto {_mostrar(real)}")
    return errores


def assert_expected(
    resp: requests.Response, expected: dict[str, Any], sent_body: Any = None
) -> None:
    """Verifica ``resp`` contra ``expected``; lanza ``AssertionError`` con todas las diferencias."""
    __tracebackhide__ = True  # el fallo se muestra en el paso, no dentro del helper
    _validar_expected(expected)
    errores: list[str] = []

    if (status := expected.get("status")) is not None:
        aceptados = status if isinstance(status, list) else [status]
        if resp.status_code not in aceptados:
            esperado = aceptados[0] if len(aceptados) == 1 else f"uno de {aceptados}"
            errores.append(f"status: esperado {esperado}, obtenido {resp.status_code}")

    real_ms = resp.elapsed.total_seconds() * 1000
    if (max_ms := expected.get("max_time_ms")) is not None and real_ms > max_ms:
        errores.append(f"tiempo: {real_ms:.0f} ms > máximo {max_ms} ms")
    if (min_ms := expected.get("min_time_ms")) is not None and real_ms < min_ms:
        errores.append(f"tiempo: {real_ms:.0f} ms < mínimo {min_ms} ms")

    for nombre, patron in (expected.get("headers") or {}).items():
        valor = resp.headers.get(nombre)
        if valor is None or not re.search(patron, valor):
            errores.append(f"cabecera {nombre}: {valor!r} no cumple /{patron}/")

    if expected.get("body_empty"):
        if resp.content:
            errores.append(f"se esperaba cuerpo vacío, llegó {resp.text[:100]!r}")
    elif CLAVES_CUERPO & set(expected):
        try:
            body = resp.json()
        except ValueError:
            errores.append(f"la respuesta no es JSON: {resp.text[:200]!r}")
        else:
            errores += _errores_cuerpo(body, expected, sent_body)

    if errores:
        detalle = "\n  - ".join(errores)
        raise AssertionError(
            f"{resp.request.method} {resp.url} -> {resp.status_code}\n  - {detalle}"
        )
