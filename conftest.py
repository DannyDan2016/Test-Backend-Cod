"""Configuración raíz de pytest: opción --env, hooks de BDD y fixtures de sesión."""

from collections.abc import Callable, Iterator
from typing import Any

import pytest

from api.reqres import ReqResClient, UsersService
from config.settings import Settings, load_settings
from support.api_key_policy import apply_api_key_policy
from support.bdd_tags import apply_tag, mark_known_bugs
from support.data_loader import TestData


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Ambiente objetivo (tiene prioridad sobre la variable TEST_ENV). Ej.: prod, staging",
    )


def _settings_de(config: pytest.Config) -> Settings:
    return load_settings(config.getoption("--env"))


def pytest_report_header(config: pytest.Config) -> list[str]:
    """Cabecera del informe: ambiente y si hay key (nunca su valor)."""
    ajustes = _settings_de(config)
    key = "definida" if ajustes.reqres_api_key else "NO definida (se omiten los @requiere_key)"
    return [f"ambiente: {ajustes.env} | ReqRes: {ajustes.reqres_base_url} | REQRES_API_KEY: {key}"]


def pytest_bdd_apply_tag(tag: str, function: Callable[..., Any]) -> bool | None:
    """Gestiona @tc-*, @known-bug y @bug:* sin crear marcadores sin registrar."""
    return apply_tag(tag, function)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    # trylast: se ejecuta después de la deselección por -m/-k, sobre los items que van a correr
    ajustes = _settings_de(config)
    mark_known_bugs(items, ajustes.env)
    apply_api_key_policy(items, ajustes)


@pytest.fixture(scope="session")
def settings(request: pytest.FixtureRequest) -> Settings:
    """Configuración del ambiente seleccionado, cargada una sola vez por sesión."""
    return _settings_de(request.config)


@pytest.fixture(scope="session")
def test_data(settings: Settings) -> TestData:
    """Datos de prueba y valores esperados del ambiente (data/comun + data/<env>)."""
    return TestData(settings.env)


@pytest.fixture(scope="session")
def reqres_client(settings: Settings) -> Iterator[ReqResClient]:
    """Cliente de ReqRes compartido por la sesión; cierra la conexión al terminar."""
    with ReqResClient.from_settings(settings) as cliente:
        yield cliente


@pytest.fixture(scope="session")
def users_service(reqres_client: ReqResClient) -> UsersService:
    """Service object de ``/users`` sobre el cliente de la sesión."""
    return UsersService(reqres_client)
