import sys
import os
import pytest
from pages.api_client import APIClient

# Agregar la ruta del proyecto a sys.path para asegurar que se puedan importar módulos correctamente
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="session")
def cliente_api():
    """Fixture que crea y proporciona una instancia de APIClient para usar en las pruebas."""
    return APIClient()



