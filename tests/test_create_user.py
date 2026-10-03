import pytest


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
            ["name", "job", "id", "createdAt"],
        ),
        (
            '{ "name": "Daniel Bernal", "job": "Prueba Automatización", '
            '"gender": "Masculino", "age": 33,}',
            400,
            [],
        ),
    ],
)
def test_crear_usuario(reqres_client, datos_usuario, estado_esperado, campos_respuesta_esperados):
    """Prueba la creación de usuarios con diferentes casos de datos de entrada."""
    respuesta = reqres_client.create_user(datos_usuario)

    # Validar que el código de estado HTTP sea el esperado
    assert respuesta.status_code == estado_esperado, (
        f"Error: esperado {estado_esperado}, obtenido {respuesta.status_code}"
    )

    # Validar que la respuesta contenga los campos esperados solo si el estado es exitoso (201)
    if respuesta.status_code == 201:
        respuesta_json = respuesta.json()
        for campo in campos_respuesta_esperados:
            assert campo in respuesta_json, f"Falta el campo {campo} en la respuesta"

        # Verificar que, si el payload es un diccionario con 'age', sea un número entero
        if isinstance(datos_usuario, dict) and "age" in datos_usuario:
            assert isinstance(datos_usuario["age"], int), (
                "El campo 'age' no es un número entero en la solicitud"
            )
