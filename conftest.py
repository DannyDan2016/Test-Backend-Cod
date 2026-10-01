import pytest

from config.settings import Settings, load_settings
from pages.api_client import APIClient


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Ambiente objetivo (tiene prioridad sobre la variable TEST_ENV). Ej.: prod",
    )


@pytest.fixture(scope="session")
def settings(request: pytest.FixtureRequest) -> Settings:
    """Configuración del ambiente seleccionado, cargada una sola vez por sesión."""
    return load_settings(request.config.getoption("--env"))


@pytest.fixture(scope="session")
def cliente_api():
    """Fixture que crea y proporciona una instancia de APIClient para usar en las pruebas."""
    return APIClient()
