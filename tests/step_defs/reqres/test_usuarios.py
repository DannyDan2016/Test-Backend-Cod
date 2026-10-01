"""Pasos de la feature de usuarios de ReqRes."""

from pytest_bdd import scenarios, when

from api.reqres import UsersService
from support.context import ScenarioContext

scenarios("reqres/usuarios.feature")


@when("consulto el listado de usuarios del caso")
def list_users(users_service: UsersService, ctx: ScenarioContext):
    ctx.response = users_service.list(**ctx.require_case().query)


@when("consulto el usuario del caso")
def get_user(users_service: UsersService, ctx: ScenarioContext):
    ctx.response = users_service.get(ctx.require_case().path_params["id"])


@when("creo el usuario del caso")
def create_user(users_service: UsersService, ctx: ScenarioContext):
    ctx.sent_body = ctx.require_case().body
    ctx.response = users_service.create(ctx.sent_body)
