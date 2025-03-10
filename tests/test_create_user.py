import sys
import os
import pytest
from pages.api_client import APIClient

# Crear una instancia del cliente API
cliente_api = APIClient()

@pytest.mark.parametrize("datos_usuario, estado_esperado, campos_respuesta_esperados", [
    ({"name": "John Arias", "job": "Ingeniero de Software"}, 201, ["name", "job", "id", "createdAt"]),
    ({"name": "Daniel Bernal", "job": "Prueba Automatización", "gender": "Masculino", "age": 33}, 201, ["name", "job", "id", "createdAt"]),
    ('{ "name": "Daniel Bernal", "job": "Prueba Automatización", "gender": "Masculino", "age": 33,}', 400, [])
])
def test_crear_usuario(datos_usuario, estado_esperado, campos_respuesta_esperados):
    """Prueba la creación de usuarios con diferentes casos de datos de entrada."""
    respuesta = cliente_api.create_user(datos_usuario)
    
    # Validar que el código de estado HTTP sea el esperado
    assert respuesta.status_code == estado_esperado, f"Error: esperado {estado_esperado}, obtenido {respuesta.status_code}"
    
    # Validar que la respuesta contenga los campos esperados solo si el estado es exitoso (201)
    if respuesta.status_code == 201:
        respuesta_json = respuesta.json()
        for campo in campos_respuesta_esperados:
            assert campo in respuesta_json, f"Falta el campo {campo} en la respuesta"
        
        # Verificar que si 'age' está en los datos de usuario y es un diccionario, sea un número entero
        if isinstance(datos_usuario, dict) and "age" in datos_usuario:
            assert isinstance(datos_usuario["age"], int), "El campo 'age' no es un número entero en la solicitud"




