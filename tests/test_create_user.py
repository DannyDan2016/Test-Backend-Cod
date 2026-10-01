import pytest

JSON_MALFORMADO = (
    '{ "name": "Daniel Bernal", "job": "Prueba Automatización", "gender": "Masculino", "age": 33,}'
)


@pytest.mark.parametrize(
    ("datos_usuario", "estado_esperado", "campos_respuesta_esperados"),
    [
        (
            {"name": "John Arias", "job": "Ingeniero de Software"},
            201,
            ["name", "job", "id", "createdAt"],
        ),
        (
            {
                "name": "Daniel Bernal",
                "job": "Prueba Automatización",
                "gender": "Masculino",
                "age": 33,
            },
            201,
            ["name", "job", "gender", "age", "id", "createdAt"],
        ),
    ],
)
def test_crear_usuario(users_service, datos_usuario, estado_esperado, campos_respuesta_esperados):
    """Prueba la creación de usuarios con diferentes casos de datos de entrada."""
    respuesta = users_service.create(datos_usuario)

    assert respuesta.status_code == estado_esperado, (
        f"Error: esperado {estado_esperado}, obtenido {respuesta.status_code}"
    )

    respuesta_json = respuesta.json()
    for campo in campos_respuesta_esperados:
        assert campo in respuesta_json, f"Falta el campo {campo} en la respuesta"

    # El eco de la respuesta debe conservar valores y tipos del payload (p. ej. age entero)
    for campo, valor in datos_usuario.items():
        assert respuesta_json[campo] == valor
        assert type(respuesta_json[campo]) is type(valor)


def test_crear_usuario_con_json_malformado(users_service):
    """Un cuerpo JSON realmente malformado (coma final) se rechaza con ``invalid_json``."""
    respuesta = users_service.create_raw(JSON_MALFORMADO)

    assert respuesta.status_code == 400
    assert respuesta.json()["error"] == "invalid_json"
