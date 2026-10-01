"""Pasos de la feature de reservas de restful-booker."""

from pytest_bdd import given, parsers, scenarios, when

from api.booker import BookingService
from support.context import ScenarioContext
from support.data_loader import TestData

scenarios("booker/reservas.feature")


@given("que restful-booker está disponible")
def booker_is_available(booker_available: None):
    """El fixture hace el warm-up con /ping y omite el escenario si la API no responde."""


@given("que dispongo de un token de autenticación válido")
def valid_token(booker_token: str):
    """El fixture obtiene el token una vez por sesión y falla si /auth no lo devuelve."""


@when(parsers.parse('creo una reserva según el caso "{clave}"'))
def create_booking(
    clave: str,
    test_data: TestData,
    booking_service: BookingService,
    created_bookings: list[int],
    ctx: ScenarioContext,
):
    ctx.case = test_data.case(clave)
    ctx.sent_body = ctx.case.body
    ctx.response = booking_service.create(ctx.sent_body)
    if ctx.response.ok and (booking_id := ctx.response.json().get("bookingid")):
        ctx.resource_id = booking_id
        created_bookings.append(booking_id)


@when(parsers.parse('consulto la reserva creada según el caso "{clave}"'))
def get_booking(
    clave: str, test_data: TestData, booking_service: BookingService, ctx: ScenarioContext
):
    # sent_body se conserva: la consulta se compara con los últimos datos enviados
    ctx.case = test_data.case(clave)
    ctx.response = booking_service.get(ctx.require_resource_id())


@when(parsers.parse('actualizo la reserva creada con el token según el caso "{clave}"'))
def update_booking(
    clave: str,
    test_data: TestData,
    booking_service: BookingService,
    booker_token: str,
    ctx: ScenarioContext,
):
    ctx.case = test_data.case(clave)
    ctx.sent_body = ctx.case.body
    ctx.response = booking_service.update(ctx.require_resource_id(), ctx.sent_body, booker_token)


@when(parsers.parse('borro la reserva creada con el token según el caso "{clave}"'))
def delete_booking(
    clave: str,
    test_data: TestData,
    booking_service: BookingService,
    booker_token: str,
    ctx: ScenarioContext,
):
    ctx.case = test_data.case(clave)
    ctx.sent_body = None
    ctx.response = booking_service.delete(ctx.require_resource_id(), booker_token)
