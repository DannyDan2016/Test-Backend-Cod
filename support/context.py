"""Contexto compartido entre los pasos de un escenario BDD."""

from dataclasses import dataclass
from typing import Any

import requests

from support.data_loader import Case


@dataclass
class ScenarioContext:
    """Estado de un escenario: caso cargado, última respuesta y cuerpo enviado."""

    case: Case | None = None
    response: requests.Response | None = None
    sent_body: Any = None

    def require_case(self) -> Case:
        if self.case is None:
            raise RuntimeError("El escenario no cargó ningún caso: falta el paso 'Dado el caso...'")
        return self.case

    def require_response(self) -> requests.Response:
        if self.response is None:
            raise RuntimeError("El escenario no hizo ninguna petición antes de verificar")
        return self.response
