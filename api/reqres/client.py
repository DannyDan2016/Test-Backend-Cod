"""Cliente de transporte de ReqRes: URL base, timeout y cabecera ``x-api-key``."""

from typing import Self

from api.base_client import BaseClient
from config.settings import Settings


class ReqResClient(BaseClient):
    """Transporte de ReqRes. Las operaciones de negocio viven en los service objects."""

    @classmethod
    def from_settings(cls, settings: Settings, api_key: str | None = None) -> Self:
        """Crea el cliente del ambiente; ``api_key`` sustituye a la key configurada si se indica."""
        return cls(
            base_url=settings.reqres_base_url,
            timeout=settings.request_timeout_s,
            api_key=api_key if api_key is not None else settings.reqres_api_key,
        )
