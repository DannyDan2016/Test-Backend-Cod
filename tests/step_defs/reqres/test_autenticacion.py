"""Pasos de la feature de registro e inicio de sesión de ReqRes."""

from pytest_bdd import scenarios, when

from api.reqres import AuthService
from support.context import ScenarioContext

scenarios("reqres/autenticacion.feature")


@when("me registro con los datos del caso")
def register(auth_service: AuthService, ctx: ScenarioContext):
    ctx.sent_body = ctx.require_case().body
    ctx.response = auth_service.register(ctx.sent_body)


@when("inicio sesión con los datos del caso")
def login(auth_service: AuthService, ctx: ScenarioContext):
    ctx.sent_body = ctx.require_case().body
    ctx.response = auth_service.login(ctx.sent_body)
