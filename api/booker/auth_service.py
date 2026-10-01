"""Service object de autenticación de restful-booker (``/auth``)."""

import requests

from api.base_client import BaseClient


class AuthService:
    """Obtención de tokens. Devuelve la ``Response`` sin hacer aserciones."""

    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def create_token(self, username: str, password: str) -> requests.Response:
        """``POST /auth``: devuelve ``{"token": ...}`` con credenciales válidas."""
        return self.client.post("/auth", json={"username": username, "password": password})
