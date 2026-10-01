from collections.abc import Iterator

import pytest

from api.reqres_client import ReqResClient
from config.settings import Settings, load_settings


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
def reqres_client(settings: Settings) -> Iterator[ReqResClient]:
    """Cliente de ReqRes compartido por la sesión; cierra la conexión al terminar."""
    with ReqResClient.from_settings(settings) as cliente:
        yield cliente
