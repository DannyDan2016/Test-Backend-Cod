"""Cliente HTTP base: capa de transporte común a todas las APIs bajo prueba.

Los clientes concretos (ReqRes, restful-booker...) heredan de ``BaseClient`` y exponen un
método por operación del API que devuelve la ``Response`` sin hacer aserciones: las
verificaciones pertenecen a los tests.
"""

from typing import Any, Self

import requests


class BaseClient:
    """Envuelve una ``requests.Session`` con URL base, timeout y cabeceras por defecto."""

    USER_AGENT = "test-backend-cod-qa/1.0"
    API_KEY_HEADER = "x-api-key"

    def __init__(
        self,
        base_url: str,
        timeout: float,
        api_key: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "User-Agent": self.USER_AGENT})
        # La cabecera solo se envía si hay key: una key vacía o inválida provoca un 403
        if api_key:
            self.session.headers[self.API_KEY_HEADER] = api_key
        if headers:
            self.session.headers.update(headers)

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Envía la petición aplicando el timeout por defecto si no se indica otro."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, self._url(path), **kwargs)

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        """Cierra la sesión y libera sus conexiones."""
        self.session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
