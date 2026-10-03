"""Adjunta a Allure cada intercambio HTTP (petición y respuesta) sin exponer secretos.

Se registra como *response hook* de ``requests.Session``. Solo se adjuntan método, URL, status,
tiempo, ``Content-Type`` y cuerpos: nunca las cabeceras de la petición, para que la
``x-api-key`` o los tokens de sesión no acaben en el reporte publicado.
"""

import contextlib
import json
from typing import Any

import allure
import requests

LIMITE_CUERPO = 5000


def _cuerpo(contenido: bytes | str | None) -> str:
    if not contenido:
        return "(vacío)"
    texto = contenido.decode("utf-8", "replace") if isinstance(contenido, bytes) else contenido
    with contextlib.suppress(ValueError):
        texto = json.dumps(json.loads(texto), ensure_ascii=False, indent=2)
    return texto[:LIMITE_CUERPO]


def attach_exchange(resp: requests.Response, *args: Any, **kwargs: Any) -> requests.Response:
    """Response hook: adjunta el intercambio y devuelve la respuesta sin modificarla."""
    peticion = resp.request
    texto = (
        f"{peticion.method} {peticion.url}\n"
        f"-> {resp.status_code} {resp.reason} en {resp.elapsed.total_seconds() * 1000:.0f} ms\n"
        f"Content-Type: {resp.headers.get('Content-Type', '-')}\n\n"
        f"--- Cuerpo enviado ---\n{_cuerpo(peticion.body)}\n\n"
        f"--- Cuerpo recibido ---\n{_cuerpo(resp.content)}\n"
    )
    allure.attach(
        texto,
        name=f"{peticion.method} {resp.status_code}",
        attachment_type=allure.attachment_type.TEXT,
    )
    return resp
