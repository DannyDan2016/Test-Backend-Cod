# Estrategia de pruebas

## 1. Alcance

| Sistema | Qué es | En alcance | Fuera de alcance |
|---|---|---|---|
| **ReqRes** (`https://reqres.in/api`) | API mock con OpenAPI 2.1.0 (66 operaciones) | Endpoints *legacy*: `/users`, `/register`, `/login` y transversales de autenticación (api key) | Colecciones, app-users y `/app/*` (inventariados, pendientes); custom endpoints (requieren configuración manual); Agent y Payments Sandbox |
| **restful-booker** (`https://restful-booker.herokuapp.com`) | Playground con CRUD real, autenticación por token y bugs intencionados | `/ping`, `/auth` y CRUD de `/booking` | Filtros de búsqueda, XML y Basic auth (inventariados) |

La suite es una **muestra curada**, no una cobertura total. El inventario completo, con unos 124 casos, sirve de mapa. De él se automatizaron los casos que demuestran más técnicas con menos escenarios y que cubren los riesgos más altos.

## 2. Criterio de selección

Cada escenario se eligió por al menos uno de estos motivos:

1. **Riesgo de negocio:** operaciones que un consumidor usa siempre (listar, consultar, crear y autenticarse) y el ciclo de vida completo de un recurso con persistencia real.
2. **Técnica de prueba:** que la muestra cubra contrato, particiones de equivalencia (esquemas ok/ko), valores límite de paginación, negativos, seguridad, rendimiento y E2E.
3. **Evidencia de criterio:** los bugs reales se automatizan verificando el comportamiento **correcto** y se marcan como `xfail(strict=True)`, no se esconden ni se adaptan a lo observado.
4. **Coste y estabilidad:** pocas peticiones por ejecución (unas 20 a ReqRes en una regresión completa, por la cuota de la key) y datos propios en booker.

## 3. Inventario y automatización por área

| Área | IDs | Casos inventariados | Automatizados | Notas |
|---|---|---|---|---|
| ReqRes legacy (users, unknown, register, login, logout y transversales) | TC-API-001 a 058 | 58 | 25 | Ver la matriz de trazabilidad |
| ReqRes con cuenta (colecciones, app-users, `/app/*`) | TC-API-100 a 129 | 30 | 0 | Dependen de la key y del plan; siguiente ampliación |
| ReqRes custom endpoints (solo 401/404) | - | 2 | 0 | Requieren configurarlos a mano en el dashboard |
| ReqRes Agent Sandbox | TC-API-150 a 157 | 8 | 0 | Opcional |
| restful-booker | TC-API-200 a 225 | 26 | 4 | Flujo E2E y 2 bugs |
| **Total** | | **124** | **29** | 17 escenarios Gherkin y 22 casos ejecutables |

Además, `tests/unit/` contiene 34 tests sin red: del cargador de datos, del helper de aserción, de la traducción de tags y la validación estática de todos los YAML y contratos en cada ambiente.

## 4. Matriz de trazabilidad

| TC | Caso | Feature / escenario | Técnica | Prioridad |
|---|---|---|---|---|
| TC-API-001 | Listado por defecto: página 1, 6 de 12 | `reqres/usuarios` · Listar usuarios por página (Primera página) | Paginación, valores exactos | smoke |
| TC-API-002 | Página 2: ids 7 a 12 | `reqres/usuarios` · Listar usuarios por página (Segunda página) | Paginación | regression |
| TC-API-007 | Contrato del listado | `reqres/usuarios` · Listar usuarios por página | Contrato | smoke |
| TC-API-009 | `delay=3` dentro del umbral | `reqres/robustez` · Una respuesta con retardo llega dentro del umbral | Rendimiento (umbral por ambiente) | regression |
| TC-API-012 | Usuario 2 con todos sus campos | `reqres/usuarios` · Consultar un usuario existente | Valores exactos, regex | smoke |
| TC-API-013 | Contrato del usuario | `reqres/usuarios` · Consultar un usuario existente | Contrato | smoke |
| TC-API-015 | Usuario inexistente: 404 | `reqres/usuarios` · Consultar un usuario inexistente | Negativo | smoke |
| TC-API-018 | Crear usuario: eco, id y createdAt | `reqres/usuarios` · Crear un usuario con nombre y trabajo | Positivo, eco | smoke |
| TC-API-019 | JSON malformado: `invalid_json` | `reqres/robustez` · Rechazar el alta con JSON malformado | Negativo, robustez | smoke |
| TC-API-021 | Campos extra con su tipo | `reqres/usuarios` · Crear un usuario con campos adicionales | Eco con tipos | regression |
| TC-API-023 | Contrato de creación | `reqres/usuarios` · Crear un usuario con nombre y trabajo | Contrato | smoke |
| TC-API-026 | PUT: eco y updatedAt sin createdAt | `reqres/usuarios` · Reemplazar un usuario | Positivo | smoke |
| TC-API-027 | Contrato del PUT | `reqres/usuarios` · Reemplazar un usuario | Contrato | smoke |
| TC-API-030 | PATCH parcial | `reqres/usuarios` · Actualizar parcialmente un usuario | Positivo, ausencia de campos | regression |
| TC-API-032 | DELETE: 204 sin cuerpo | `reqres/usuarios` · Borrar un usuario | Positivo | smoke |
| TC-API-039 | Registro correcto | `reqres/autenticacion` · Registrar un usuario (Registro correcto) | Partición válida | smoke |
| TC-API-040 | Contrato del registro | `reqres/autenticacion` · Registrar un usuario | Contrato | smoke |
| TC-API-041 | Registro sin password | `reqres/autenticacion` · Registrar un usuario (Datos obligatorios) | Partición inválida | smoke |
| TC-API-043 | Usuario no predefinido | `reqres/autenticacion` · Registrar un usuario (Usuario no permitido) | Partición inválida | regression |
| TC-API-045 | Login correcto | `reqres/autenticacion` · Iniciar sesión (Login correcto) | Partición válida | smoke |
| TC-API-046 | Contrato del login | `reqres/autenticacion` · Iniciar sesión | Contrato | smoke |
| TC-API-047 | Login sin password | `reqres/autenticacion` · Iniciar sesión (Falta la password) | Partición inválida | smoke |
| TC-API-048 | Login sin email | `reqres/autenticacion` · Iniciar sesión (Falta el email) | Partición inválida | regression |
| TC-API-049 | Password incorrecta se rechaza | `reqres/autenticacion` · Iniciar sesión con una password incorrecta | Negativo, xfail DEV-004 | regression |
| TC-API-052 | Api key inválida: 403 | `reqres/robustez` · Rechazar una petición con una api key no reconocida | Seguridad | smoke |
| TC-API-203 | Crear reserva: 201 | `booker/reservas` · Crear una reserva responde 201 Created | xfail BKR-BUG-6 | regression |
| TC-API-216 | Borrar reserva: 200/204 | `booker/reservas` · Borrar una reserva responde sin indicar una creación | xfail BKR-BUG-3 | regression |
| TC-API-217 | GET tras DELETE: 404 | `booker/reservas` · Ciclo de vida completo | Verificación del borrado | smoke |
| TC-API-225 | Flujo E2E con token | `booker/reservas` · Ciclo de vida completo de una reserva autenticada con token | E2E, persistencia, contrato | smoke |

La relación TC ↔ caso también está en los datos: cada caso de `data/` lleva su `id`. El paso `Dado el caso de prueba` falla si ese `id` no coincide con un `@tc-*` del escenario.

## 5. Bugs y desviaciones encontrados

Fecha de las observaciones: 2026-10-01.

### Automatizados como `@known-bug` (xfail estricto)

| ID | Endpoint | Esperado | Observado | Evidencia (`pytest --runxfail -m known_bug`) |
|---|---|---|---|---|
| DEV-004 | ReqRes `POST /api/login` con un usuario predefinido y una password incorrecta | 400/401 con error y sin token | 200 con token | `POST https://reqres.in/api/login -> 200` |
| BKR-BUG-6 | restful-booker `POST /booking` | 201 Created | 200 OK | `status: esperado 201, obtenido 200` |
| BKR-BUG-3 | restful-booker `DELETE /booking/{id}` | 200 o 204 | 201 Created | `status: esperado uno de [200, 204], obtenido 201` |

### Desviaciones de la spec documentadas (sin xfail en la muestra)

| ID | Endpoint | Spec | Observado | Tratamiento |
|---|---|---|---|---|
| DEV-001 | `GET /api/users/{id}` inexistente | 404 con `ErrorResponse` | 404 con `{}` | TC-API-015 verifica el 404 con `{}` y documenta la desviación |
| DEV-002 / DEV-003 | `?page=0`, `?page=abc` y `?per_page=101` | 400 por `minimum`/`maximum` | 200 normalizado | Inventariados (TC-API-005 y 006) |
| DEV-005 | Endpoints legacy | `x-api-key` obligatoria | Responden sin key (cuota anónima) | La suite usa siempre la key |

### Falso positivo corregido en la suite original (H-01)

El caso "JSON inválido" pasaba un `str` con `json=`. requests lo serializa como un string JSON **válido**, así que la API lo rechazaba por no ser un objeto, no por estar malformado: el test pasaba por la razón equivocada. Ahora `UsersService.create_raw` envía el cuerpo tal cual y TC-API-019 comprueba `error == "invalid_json"`. También se eliminó una aserción tautológica que validaba el tipo de `age` en el payload de entrada en lugar de en la respuesta (H-02).

### Otros bugs de restful-booker inventariados y no automatizados

| ID | Endpoint | Esperado | Observado |
|---|---|---|---|
| BKR-BUG-1 | `POST /auth` con credenciales malas | 401 | 200 con `{"reason": "Bad credentials"}` |
| BKR-BUG-2 | `PUT /booking/{id}` inexistente | 404 | 405 |
| BKR-BUG-4 | `POST /booking` sin campos obligatorios | 400 | 500 |
| BKR-BUG-5 | `totalprice` negativo o checkout anterior al checkin | 400 | 200 |

## 6. Datos, ambientes y estabilidad

- **Datos y esperados en YAML** (`data/comun` + `data/<env>`). Los pasos no llevan literales de negocio. Un meta-control rechaza las claves desconocidas (`expectd`, `json_equal`...) para que una errata no se ignore.
- **restful-booker:** cada escenario crea su reserva y un fixture la borra al terminar si sigue viva. Nunca se usan ids fijos. Antes de empezar se hace un warm-up con `/ping` y un timeout amplio.
- **Sin esperas fijas:** los tiempos se miden con `Response.elapsed` y se comparan con umbrales del YAML. No hay reintentos que oculten fallos.
- **Secretos:** la key solo se lee vía `config/settings.py`. No se imprime (la cabecera de pytest solo dice "definida") ni se adjunta a Allure, que nunca recibe las cabeceras de la petición.

## 7. Siguientes pasos propuestos

1. Colecciones y app-users de ReqRes (TC-API-100 a 129), con un ambiente `dev` real mediante `X-Reqres-Env`.
2. Resto de restful-booker (filtros, XML, Basic auth y BKR-BUG-1/2/4/5).
3. Medir la cobertura de operaciones y de pares operación-status contra la OpenAPI versionada y publicarla en el resumen del job.
4. Historial de Allure entre ejecuciones de Pages.
