# Imagen para ejecutar la suite de pruebas de API de forma reproducible.
# Python 3.12 alineado con .python-version y con target-version de ruff (py312).
FROM python:3.12-slim

# Sin archivos .pyc y con la salida de pytest sin buffer (logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# UID/GID del usuario sin privilegios. Se pueden ajustar al usuario del host
# (HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose build) para que
# los resultados escritos en el volumen ./reports pertenezcan a ese usuario en Linux.
ARG UID=1000
ARG GID=1000

WORKDIR /app

# Solo dependencias de ejecución; se copian primero para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd --gid "${GID}" qa \
    && useradd --uid "${UID}" --gid "${GID}" --create-home --shell /usr/sbin/nologin qa

# El código queda en propiedad de root (solo lectura para el usuario qa);
# .dockerignore impide que .env, .venv o reportes antiguos entren en la imagen.
COPY . .

# Único directorio escribible: aquí escribe pytest los resultados de Allure
RUN mkdir -p /app/reports && chown qa:qa /app/reports

USER qa

# -p no:cacheprovider: /app no es escribible y la caché de pytest no aporta nada en un contenedor.
# --clean-alluredir: cada ejecución parte de reports/allure-results vacío, así el reporte
# de Allure refleja solo la última ejecución y no mezcla resultados antiguos del volumen.
ENTRYPOINT ["pytest", "-p", "no:cacheprovider", "--clean-alluredir"]
