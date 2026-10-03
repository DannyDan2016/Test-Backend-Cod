"""Service object del health check de restful-booker (``/ping``)."""

import requests

from api.base_client import BaseClient


class HealthService:
    """Comprobación de disponibilidad. Devuelve la ``Response`` sin hacer aserciones."""

    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def ping(self, timeout: float | None = None) -> requests.Response:
        """``GET /ping``. ``timeout`` permite un warm-up más largo (Heroku puede estar en frío)."""
        if timeout is None:
            return self.client.get("/ping")
        return self.client.get("/ping", timeout=timeout)
