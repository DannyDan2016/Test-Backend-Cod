# Cómo contribuir

## Flujo

1. Crea una rama desde `main` con el formato `tipo/descripcion-kebab` (`feat`, `fix`, `test`, `refactor`, `ci`, `build`, `docs`, `chore`).
2. Haz commits atómicos en [Conventional Commits](https://www.conventionalcommits.org/es/): tipo en inglés y descripción en español, p. ej. `test(usuarios): cubre el listado paginado`.
3. Antes de abrir el PR, comprueba que estos comandos pasan:
   ```bash
   docker compose run --rm lint
   docker compose run --rm api-tests -m "smoke or unit"
   ```
4. Rellena la plantilla del PR.

## Convenciones

**Service objects (`api/`)**
- Un servicio por recurso y un método por operación. Devuelven la `Response` sin hacer aserciones.
- Las URLs y las cabeceras viven aquí, nunca en los pasos.
- El código va en inglés; los docstrings y los mensajes, en español.

**Features (`features/`)**
- Empiezan con `# language: es`. Los escenarios son declarativos: un caso, una acción y una verificación.
- Tags obligatorios: una prioridad (`@smoke` o `@regression`) y un `@tc-<area>-NNN`. Añade `@negative` y el tag de técnica cuando aplique.
- En los bloques `Ejemplos` solo se pueden usar marcadores registrados: pytest-bdd no pasa esos tags por el hook. Los `@tc-*` van en el escenario.

**Datos (`data/`)**
- Cada caso tiene `id`, `descripcion`, `request` y `expected` (claves admitidas en `support/assertions.py`).
- Lo común va en `data/comun/`. En `data/<env>/` solo se declara lo que cambia en ese ambiente.
- Los textos de la API se copian literalmente, con sus erratas si las tienen. Las fechas van entre comillas.

**Contratos (`schemas/`)**
- JSON Schema draft 2020-12, derivados de la spec cuando exista. Cuando el contrato sea más estricto que la spec, explícalo en la `description`.

**Bugs del sistema bajo prueba**
- El escenario verifica el comportamiento **correcto** y lleva `@known-bug @bug:<ID>`.
- Añade la entrada correspondiente en `data/comun/bugs_conocidos.yaml`. Se ejecuta como `xfail(strict=True)`.

**Secretos**
- Los valores reales van en `.env` (ignorado) o en los secrets del repositorio. Documenta las variables nuevas en `.env.example`.
