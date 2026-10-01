"""Pasos de la feature de usuarios de ReqRes."""

from pytest_bdd import scenarios, when

from api.reqres import UsersService
from support.context import ScenarioContext

scenarios("reqres/usuarios.feature")


@when("creo el usuario del caso")
def create_user(users_service: UsersService, ctx: ScenarioContext):
    ctx.sent_body = ctx.require_case().body
    ctx.response = users_service.create(ctx.sent_body)
