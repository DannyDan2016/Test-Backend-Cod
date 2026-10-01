"""Cliente de transporte de restful-booker."""

from typing import Self

from api.base_client import BaseClient
from config.settings import Settings


class BookerClient(BaseClient):
    """Transporte de restful-booker. Las operaciones viven en los service objects."""

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(base_url=settings.booker_base_url, timeout=settings.request_timeout_s)
