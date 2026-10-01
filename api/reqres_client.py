"""Cliente de la API de ReqRes (https://reqres.in)."""

from typing import Any, Self

import requests

from api.base_client import BaseClient
from config.settings import Settings


class ReqResClient(BaseClient):
    """Operaciones de ReqRes. Cada método devuelve la ``Response`` sin hacer aserciones."""

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(
            base_url=settings.reqres_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.reqres_api_key,
        )

    def create_user(self, payload: Any) -> requests.Response:
        """Crea un usuario (``POST /users``) enviando ``payload`` serializado como JSON."""
        return self.post("/users", json=payload)
