import pytest

from pages.api_client import APIClient


@pytest.fixture(scope="session")
def cliente_api():
    """Fixture que crea y proporciona una instancia de APIClient para usar en las pruebas."""
    return APIClient()
