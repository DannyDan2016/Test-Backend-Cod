"""Service object de autenticación de ReqRes (``/register`` y ``/login``)."""

from typing import Any

import requests

from api.base_client import BaseClient


class AuthService:
    """Registro e inicio de sesión. Devuelven la ``Response`` sin hacer aserciones."""

    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def register(self, payload: dict[str, Any]) -> requests.Response:
        """Registra un usuario (``POST /register``)."""
        return self.client.post("/register", json=payload)

    def login(self, payload: dict[str, Any]) -> requests.Response:
        """Inicia sesión (``POST /login``)."""
        return self.client.post("/login", json=payload)
