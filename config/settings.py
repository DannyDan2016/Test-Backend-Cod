"""Configuración de la suite por ambiente.

Orden de precedencia de cada valor (de mayor a menor):
1. Variables de entorno del sistema (p. ej. las que inyecta la CI desde GitHub Secrets).
2. Archivo ``.env`` en la raíz del proyecto (ignorado por git; ver ``.env.example``).
3. Valores por defecto del ambiente seleccionado en ``AMBIENTES``.

Un valor vacío (``REQRES_BASE_URL=``) se trata como "no definido" y usa el valor por defecto.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]

AMBIENTE_POR_DEFECTO = "prod"
TIMEOUT_POR_DEFECTO_S = 10.0

# URLs base por ambiente. Para añadir uno nuevo basta con otra entrada y, si sus datos o
# esperados difieren, una carpeta data/<ambiente>/ con los overrides.
AMBIENTES: dict[str, dict[str, str]] = {
    "prod": {
        "reqres_base_url": "https://reqres.in/api",
        "booker_base_url": "https://restful-booker.herokuapp.com",
    },
    # Ambiente de ejemplo: las APIs públicas no tienen staging, así que apunta a las mismas URLs
    # (sobrescribibles desde .env) y demuestra los overrides de data/staging/ (p. ej. umbrales
    # de tiempo más holgados).
    "staging": {
        "reqres_base_url": "https://reqres.in/api",
        "booker_base_url": "https://restful-booker.herokuapp.com",
    },
}


@dataclass(frozen=True)
class Settings:
    """Valores de configuración resueltos para una ejecución de la suite."""

    env: str
    reqres_base_url: str
    booker_base_url: str
    request_timeout_s: float
    # repr=False evita que la key aparezca en logs o en mensajes de error de pytest
    reqres_api_key: str | None = field(default=None, repr=False)


def _leer(nombre: str, por_defecto: str) -> str:
    """Devuelve la variable de entorno ``nombre`` o ``por_defecto`` si no existe o está vacía."""
    valor = os.getenv(nombre, "").strip()
    return valor or por_defecto


def _leer_opcional(nombre: str) -> str | None:
    """Devuelve la variable de entorno ``nombre`` o ``None`` si no existe o está vacía."""
    valor = os.getenv(nombre, "").strip()
    return valor or None


def _leer_float(nombre: str, por_defecto: float) -> float:
    """Devuelve la variable ``nombre`` como número positivo, con un error claro si no lo es."""
    crudo = _leer(nombre, str(por_defecto))
    try:
        valor = float(crudo)
    except ValueError as error:
        raise ValueError(f"{nombre} debe ser un número (recibido: {crudo!r})") from error
    if valor <= 0:
        raise ValueError(f"{nombre} debe ser mayor que 0 (recibido: {valor})")
    return valor


def load_settings(env: str | None = None) -> Settings:
    """Carga la configuración del ambiente ``env`` (o ``TEST_ENV``, o el ambiente por defecto)."""
    load_dotenv(RAIZ_PROYECTO / ".env", override=False)

    ambiente = (env or _leer("TEST_ENV", AMBIENTE_POR_DEFECTO)).strip().lower()
    if ambiente not in AMBIENTES:
        disponibles = ", ".join(sorted(AMBIENTES))
        raise ValueError(f"Ambiente desconocido: {ambiente!r}. Disponibles: {disponibles}")
    por_defecto = AMBIENTES[ambiente]

    return Settings(
        env=ambiente,
        reqres_base_url=_leer("REQRES_BASE_URL", por_defecto["reqres_base_url"]).rstrip("/"),
        booker_base_url=_leer("BOOKER_BASE_URL", por_defecto["booker_base_url"]).rstrip("/"),
        request_timeout_s=_leer_float("REQUEST_TIMEOUT_S", TIMEOUT_POR_DEFECTO_S),
        reqres_api_key=_leer_opcional("REQRES_API_KEY"),
    )
