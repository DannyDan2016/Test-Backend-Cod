"""Service object del recurso ``/users`` de ReqRes."""

from typing import Any

import requests

from api.base_client import BaseClient


class UsersService:
    """Operaciones sobre usuarios. Devuelven la ``Response`` sin hacer aserciones."""

    PATH = "/users"

    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def list(
        self,
        page: int | str | None = None,
        per_page: int | str | None = None,
        delay: int | str | None = None,
    ) -> requests.Response:
        """Lista usuarios (``GET /users``). ``delay`` pide a ReqRes que retrase la respuesta."""
        params = {"page": page, "per_page": per_page, "delay": delay}
        return self.client.get(self.PATH, params={k: v for k, v in params.items() if v is not None})

    def get(self, user_id: int | str) -> requests.Response:
        """Obtiene un usuario (``GET /users/{id}``)."""
        return self.client.get(f"{self.PATH}/{user_id}")

    def create(self, payload: dict[str, Any]) -> requests.Response:
        """Crea un usuario (``POST /users``) serializando ``payload`` como JSON."""
        return self.client.post(self.PATH, json=payload)

    def create_raw(self, body: str) -> requests.Response:
        """Envía ``body`` tal cual con ``Content-Type: application/json`` (p. ej. JSON malformado).

        Con ``json=`` requests serializaría el texto como un string JSON válido, así que el
        servidor nunca vería un cuerpo realmente malformado.
        """
        return self.client.post(
            self.PATH,
            data=body.encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

    def update(self, user_id: int | str, payload: dict[str, Any]) -> requests.Response:
        """Reemplaza un usuario (``PUT /users/{id}``)."""
        return self.client.put(f"{self.PATH}/{user_id}", json=payload)

    def patch(self, user_id: int | str, payload: dict[str, Any]) -> requests.Response:
        """Actualiza parcialmente un usuario (``PATCH /users/{id}``)."""
        return self.client.patch(f"{self.PATH}/{user_id}", json=payload)

    def delete(self, user_id: int | str) -> requests.Response:
        """Borra un usuario (``DELETE /users/{id}``)."""
        return self.client.delete(f"{self.PATH}/{user_id}")
