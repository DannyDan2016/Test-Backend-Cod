"""Carga y validación de contratos JSON Schema (draft 2020-12) desde ``schemas/``."""

import json
from functools import cache
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from config.settings import RAIZ_PROYECTO

DIRECTORIO_SCHEMAS = RAIZ_PROYECTO / "schemas"


@cache
def load_validator(nombre: str) -> Draft202012Validator:
    """Devuelve el validador del contrato ``nombre`` (p. ej. ``reqres/user_response``).

    El esquema se valida a sí mismo al cargarse, para detectar contratos mal escritos.
    """
    ruta = DIRECTORIO_SCHEMAS / f"{nombre}.schema.json"
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe el contrato {nombre!r}: se esperaba {ruta}")
    esquema = json.loads(ruta.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(esquema)
    return Draft202012Validator(esquema, format_checker=FormatChecker())


def schema_errors(nombre: str, instancia: Any) -> list[str]:
    """Lista legible de incumplimientos de ``instancia`` frente al contrato ``nombre``."""
    validador = load_validator(nombre)
    return [
        f"contrato {nombre}: {error.json_path}: {error.message}"
        for error in sorted(validador.iter_errors(instancia), key=lambda e: e.json_path)
    ]
