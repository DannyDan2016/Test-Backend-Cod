"""Service object del recurso ``/booking`` de restful-booker."""

from typing import Any

import requests

from api.base_client import BaseClient


class BookingService:
    """CRUD de reservas. Devuelven la ``Response`` sin hacer aserciones.

    Las operaciones de escritura se autentican con el token de ``/auth`` en la cookie ``token``.
    """

    PATH = "/booking"

    def __init__(self, client: BaseClient) -> None:
        self.client = client

    @staticmethod
    def _auth(token: str) -> dict[str, str]:
        return {"Cookie": f"token={token}"}

    def create(self, payload: dict[str, Any]) -> requests.Response:
        """Crea una reserva (``POST /booking``)."""
        return self.client.post(self.PATH, json=payload)

    def get(self, booking_id: int | str) -> requests.Response:
        """Obtiene una reserva (``GET /booking/{id}``)."""
        return self.client.get(f"{self.PATH}/{booking_id}")

    def update(
        self, booking_id: int | str, payload: dict[str, Any], token: str
    ) -> requests.Response:
        """Reemplaza una reserva (``PUT /booking/{id}``) autenticado con ``token``."""
        return self.client.put(f"{self.PATH}/{booking_id}", json=payload, headers=self._auth(token))

    def delete(self, booking_id: int | str, token: str) -> requests.Response:
        """Borra una reserva (``DELETE /booking/{id}``) autenticado con ``token``."""
        return self.client.delete(f"{self.PATH}/{booking_id}", headers=self._auth(token))
