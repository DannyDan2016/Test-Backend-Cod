"""Pasos de la feature de robustez de ReqRes."""

from pytest_bdd import scenarios, when

from api.reqres import UsersService
from support.context import ScenarioContext

scenarios("reqres/robustez.feature")


@when("envío el cuerpo crudo del caso al alta de usuarios")
def create_user_raw(users_service: UsersService, ctx: ScenarioContext):
    ctx.response = users_service.create_raw(ctx.require_case().request["raw_body"])
