"""Política de ejecución de los escenarios que necesitan ``REQRES_API_KEY``.

- Con key: se ejecutan con normalidad.
- Sin key en local: se omiten (skip) con un motivo que explica cómo configurarla.
- Sin key en CI (``CI=true``): la sesión falla, porque un pipeline en verde sin ejecutar nada
  ocultaría el problema. Excepción: ``ALLOW_MISSING_API_KEY=true`` (p. ej. PRs desde forks, que no
  reciben secrets), donde se omiten igual que en local.
"""

import os
from collections.abc import Iterable

import pytest

from config.settings import Settings

MARCADOR = "requiere_key"
MOTIVO_SKIP = (
    "Falta REQRES_API_KEY: defínela en .env (ver .env.example) o como variable de entorno. "
    "La key gratuita se obtiene en https://app.reqres.in"
)
MENSAJE_CI = (
    "CI=true y REQRES_API_KEY no está definida: configura el secret REQRES_API_KEY en el "
    "repositorio. Si la ausencia es esperada (PR desde un fork), "
    "exporta ALLOW_MISSING_API_KEY=true."
)


def _activa(nombre: str) -> bool:
    return os.getenv(nombre, "").strip().lower() in {"1", "true", "yes"}


def apply_api_key_policy(items: Iterable[pytest.Item], settings: Settings) -> None:
    """Omite o hace fallar los escenarios marcados con ``requiere_key`` si no hay key."""
    afectados = [item for item in items if item.get_closest_marker(MARCADOR)]
    if not afectados or settings.reqres_api_key:
        return
    if _activa("CI") and not _activa("ALLOW_MISSING_API_KEY"):
        pytest.exit(MENSAJE_CI, returncode=pytest.ExitCode.USAGE_ERROR)
    for item in afectados:
        item.add_marker(pytest.mark.skip(reason=MOTIVO_SKIP))
