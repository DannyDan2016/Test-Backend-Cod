"""Pasos de la feature de seguridad y robustez de ReqRes."""

from collections.abc import Callable

from pytest_bdd import scenarios, when

from api.reqres import UsersService
from support.context import ScenarioContext

scenarios("reqres/robustez.feature")


@when("consulto el usuario del caso con la api key del caso")
def get_user_with_case_key(
    users_service_with_key: Callable[[str], UsersService], ctx: ScenarioContext
):
    caso = ctx.require_case()
    servicio = users_service_with_key(caso.request["api_key"])
    ctx.response = servicio.get(caso.path_params["id"])


@when("envío el cuerpo crudo del caso al alta de usuarios")
def create_user_raw(users_service: UsersService, ctx: ScenarioContext):
    ctx.response = users_service.create_raw(ctx.require_case().request["raw_body"])


@when("consulto el listado de usuarios con el retardo del caso")
def list_users_with_delay(users_service: UsersService, ctx: ScenarioContext):
    ctx.response = users_service.list(**ctx.require_case().query)
