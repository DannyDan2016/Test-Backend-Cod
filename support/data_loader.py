"""Cargador de datos de prueba y valores esperados en YAML, por ambiente.

Estructura::

    data/comun/<api>/<recurso>.yaml   # datos compartidos por todos los ambientes
    data/<env>/<api>/<recurso>.yaml   # overrides del ambiente (opcionales)

Cada archivo se monta en un espacio de nombres según su ruta: ``data/comun/reqres/usuarios.yaml``
queda bajo ``reqres.usuarios``. Los datos del ambiente se combinan con los comunes mediante un
merge profundo en el que gana el ambiente (las listas se sustituyen, no se concatenan).

Las claves se piden con rutas de puntos, p. ej. ``reqres.usuarios.crear_basico``. Si una clave no
existe, el error indica qué tramo falta, en qué archivos se buscó y qué claves hay disponibles.
"""

import copy
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from config.settings import RAIZ_PROYECTO

DIRECTORIO_DATOS = RAIZ_PROYECTO / "data"
CARPETA_COMUN = "comun"

# Claves permitidas en un caso de prueba y en su bloque ``request``
CLAVES_CASO = frozenset({"id", "descripcion", "request", "expected"})
CLAVES_REQUEST = frozenset({"path_params", "query", "body", "raw_body", "api_key"})


class DataError(Exception):
    """Error en los archivos de datos de prueba (YAML inválido, clave inexistente...)."""


class DataKeyError(DataError, KeyError):
    """La clave pedida no existe en los datos del ambiente."""

    def __str__(self) -> str:  # KeyError entrecomilla el mensaje; se muestra tal cual
        return str(self.args[0])


@dataclass(frozen=True)
class Case:
    """Case de prueba declarado en YAML: datos de entrada y valores esperados."""

    clave: str
    id: str | None
    descripcion: str
    request: dict[str, Any] = field(default_factory=dict)
    expected: dict[str, Any] = field(default_factory=dict)

    @property
    def body(self) -> Any:
        return self.request.get("body")

    @property
    def query(self) -> dict[str, Any]:
        return self.request.get("query") or {}

    @property
    def path_params(self) -> dict[str, Any]:
        return self.request.get("path_params") or {}


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Combina dos diccionarios recursivamente; ``override`` gana en caso de conflicto."""
    resultado = dict(base)
    for clave, valor in override.items():
        if isinstance(valor, Mapping) and isinstance(resultado.get(clave), Mapping):
            resultado[clave] = deep_merge(resultado[clave], valor)
        else:
            resultado[clave] = valor
    return resultado


def _leer_yaml(ruta: Path) -> dict[str, Any]:
    try:
        contenido = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise DataError(f"YAML inválido en {ruta}: {error}") from error
    if contenido is None:
        return {}
    if not isinstance(contenido, dict):
        raise DataError(f"{ruta} debe contener un mapa clave-valor en el primer nivel")
    return contenido


class TestData:
    """Datos de un ambiente: ``data/comun`` combinado con ``data/<env>``."""

    __test__ = False  # evita que pytest intente recolectar esta clase como test

    def __init__(self, env: str, base_dir: Path = DIRECTORIO_DATOS) -> None:
        self.env = env
        self.base_dir = base_dir
        if not (base_dir / CARPETA_COMUN).is_dir():
            raise DataError(f"No existe la carpeta de datos comunes: {base_dir / CARPETA_COMUN}")
        self._datos: dict[str, Any] = {}
        # Archivos de origen por espacio de nombres, para los mensajes de error
        self._origenes: dict[str, list[Path]] = {}
        self._cargar(base_dir / CARPETA_COMUN)
        self._cargar(base_dir / env)

    def _cargar(self, carpeta: Path) -> None:
        if not carpeta.is_dir():
            return
        for ruta in sorted(carpeta.rglob("*.yaml")):
            partes = ruta.relative_to(carpeta).with_suffix("").parts
            nodo = self._datos
            for parte in partes[:-1]:
                nodo = nodo.setdefault(parte, {})
            nodo[partes[-1]] = deep_merge(nodo.get(partes[-1], {}), _leer_yaml(ruta))
            relativa = ruta.relative_to(self.base_dir.parent).as_posix()
            self._origenes.setdefault(".".join(partes), []).append(Path(relativa))

    def _origen(self, ruta: str) -> str:
        """Archivos YAML que aportan datos al prefijo más largo de ``ruta``."""
        partes = ruta.split(".")
        for fin in range(len(partes), 0, -1):
            prefijo = ".".join(partes[:fin])
            if prefijo in self._origenes:
                return ", ".join(p.as_posix() for p in self._origenes[prefijo])
        return f"ningún archivo bajo {self.base_dir.name}/{{{CARPETA_COMUN},{self.env}}}"

    def get_all(self) -> dict[str, Any]:
        """Copia de todos los datos combinados del ambiente."""
        return copy.deepcopy(self._datos)

    def get(self, clave: str) -> Any:
        """Devuelve el valor de ``clave`` (ruta con puntos) o lanza un error explicativo."""
        nodo: Any = self._datos
        recorrido: list[str] = []
        for parte in clave.split("."):
            if not isinstance(nodo, dict) or parte not in nodo:
                contexto = ".".join(recorrido) or "(raíz)"
                disponibles = ", ".join(sorted(nodo)) if isinstance(nodo, dict) else "-"
                raise DataKeyError(
                    f"No existe la clave {clave!r} en los datos del ambiente {self.env!r}: "
                    f"falta {parte!r} dentro de {contexto!r} (archivos: {self._origen(clave)}). "
                    f"Claves disponibles: {disponibles}"
                )
            nodo = nodo[parte]
            recorrido.append(parte)
        return nodo

    def case(self, clave: str) -> Case:
        """Devuelve el caso ``clave`` validando su estructura (detecta erratas en el YAML)."""
        crudo = self.get(clave)
        origen = self._origen(clave)
        if not isinstance(crudo, dict):
            raise DataError(f"El caso {clave!r} ({origen}) debe ser un mapa")
        if desconocidas := set(crudo) - CLAVES_CASO:
            raise DataError(
                f"El caso {clave!r} ({origen}) tiene claves no permitidas: "
                f"{sorted(desconocidas)}. Permitidas: {sorted(CLAVES_CASO)}"
            )
        request = crudo.get("request") or {}
        if desconocidas := set(request) - CLAVES_REQUEST:
            raise DataError(
                f"El bloque request del caso {clave!r} ({origen}) tiene claves no permitidas: "
                f"{sorted(desconocidas)}. Permitidas: {sorted(CLAVES_REQUEST)}"
            )
        return Case(
            clave=clave,
            id=crudo.get("id"),
            descripcion=crudo.get("descripcion", ""),
            request=request,
            expected=crudo.get("expected") or {},
        )
