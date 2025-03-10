## Test-Backend-Cod

Este repositorio, "Test-Backend-Cod", contiene un proyecto de automatización de pruebas para la API de ReqRes, utilizando Python, Pytest y Requests. El objetivo es validar la creación de usuarios y verificar las respuestas de la API, siguiendo buenas prácticas como el Page Object Model (POM).

## Tecnologías Utilizadas

Python: Lenguaje de programación para escribir las pruebas.
Pytest: Framework para ejecutar pruebas unitarias y generar reportes.
Requests: Biblioteca para realizar peticiones HTTP a la API.

## Estructura del Proyecto

La estructura del proyecto está organizada de la siguiente manera:

Test-Backend-Cod/
├── pages/
│   ├── api_client.py  # Cliente API para manejar peticiones HTTP
│   └── __init__.py
├── tests/
│   ├── test_create_user.py  # Pruebas de creación de usuario
│   └── __init__.py
├── reportes/  # Directorio para el reporte
├── test_backend_QA_Vid.mp4  # Video de la ejecución de las pruebas
├── requirements.txt  # Dependencias del proyecto
├── README.md  # Documentación del proyecto
└── pytest.ini  # Configuración de Pytest


## Instalación y Configuración

Sigue estos pasos para configurar el proyecto:

1. Clonar el repositorio:

git clone https://github.com/DannyDan2016/Test-Backend-Cod
cd Test-Backend-Cod

2. Crear y activar un entorno virtual:
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate


3. Instalar dependencias:

pip install -r requirements.txt

Asegúrate de tener FFmpeg instalado en tu sistema para grabar la ejecución de las pruebas.


## Casos de Prueba

El proyecto incluye tres casos de prueba para el endpoint POST /api/users de ReqRes:

Caso Exitoso 1: Crear usuario con name y job, verificar código 201 y campos name, job, id, createdAt.
Caso Exitoso 2: Crear usuario con name, job, gender, age, verificar código 201, campos name, job, id, createdAt, y que age sea un entero.
Caso Fallido 3: Enviar JSON inválido con coma al final, verificar código 400.


## Contribuciones
Si deseas contribuir:

Haz un fork del repositorio.
Crea una nueva rama para tu contribución.
Realiza los cambios y haz commit.
Sube los cambios y abre un Pull Request para revisión.


## Licencia
Autor Danny Parrado
