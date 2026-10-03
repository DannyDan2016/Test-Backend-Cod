"""Fixtures de restful-booker: cliente, warm-up, token y limpieza de las reservas creadas."""

from collections.abc import Iterator

import pytest
import requests

from api.booker import AuthService, BookerClient, BookingService, HealthService
from config.settings import Settings
from support.allure_http import attach_exchange
from support.data_loader import TestData


@pytest.fixture(scope="session")
def booker_client(settings: Settings) -> Iterator[BookerClient]:
    with BookerClient.from_settings(settings) as cliente:
        cliente.session.hooks["response"].append(attach_exchange)
        yield cliente


@pytest.fixture(scope="session")
def booker_available(booker_client: BookerClient, test_data: TestData) -> None:
    """Warm-up con ``/ping``: Heroku puede tardar en arrancar si la app estaba en frío.

    Si no responde, los escenarios se omiten con el motivo: es una API pública de terceros y
    su caída no es un fallo de la suite.
    """
    warmup = test_data.get("booker.servicio.warmup")
    try:
        resp = HealthService(booker_client).ping(timeout=warmup["timeout_s"])
    except requests.RequestException as error:
        pytest.skip(f"restful-booker no disponible ({type(error).__name__}): {error}")
    if resp.status_code not in warmup["status_disponible"]:
        pytest.skip(f"restful-booker no disponible: /ping respondió {resp.status_code}")


@pytest.fixture(scope="session")
def booker_token(booker_client: BookerClient, test_data: TestData) -> str:
    """Token de la sesión, obtenido con las credenciales públicas de la API de demostración."""
    credenciales = test_data.get("booker.servicio.credenciales")
    resp = AuthService(booker_client).create_token(**credenciales)
    token = resp.json().get("token") if resp.ok else None
    if not token:
        pytest.fail(
            f"No se pudo obtener el token de restful-booker: {resp.status_code} {resp.text}"
        )
    return token


@pytest.fixture
def booking_service(booker_client: BookerClient) -> BookingService:
    return BookingService(booker_client)


@pytest.fixture
def created_bookings(booking_service: BookingService, booker_token: str) -> Iterator[list[int]]:
    """Registro de las reservas creadas por el escenario; las que sigan vivas se borran al final."""
    ids: list[int] = []
    yield ids
    for booking_id in ids:
        if booking_service.get(booking_id).status_code != 404:
            booking_service.delete(booking_id, booker_token)
