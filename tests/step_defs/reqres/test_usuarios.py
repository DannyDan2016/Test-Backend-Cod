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


@when("reemplazo el usuario del caso")
def replace_user(users_service: UsersService, ctx: ScenarioContext):
    caso = ctx.require_case()
    ctx.sent_body = caso.body
    ctx.response = users_service.update(caso.path_params["id"], caso.body)


@when("actualizo parcialmente el usuario del caso")
def patch_user(users_service: UsersService, ctx: ScenarioContext):
    caso = ctx.require_case()
    ctx.sent_body = caso.body
    ctx.response = users_service.patch(caso.path_params["id"], caso.body)


@when("borro el usuario del caso")
def delete_user(users_service: UsersService, ctx: ScenarioContext):
    ctx.response = users_service.delete(ctx.require_case().path_params["id"])
