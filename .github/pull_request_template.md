## Resumen

<!-- Qué cambia y por qué, en dos o tres líneas. -->

## Cambios

-

## Cómo probar

```bash
docker compose run --rm lint
docker compose run --rm api-tests -m smoke
```

## Resultado de la verificación

<!-- passed / failed / xfailed y, si algo falla por causas externas, la evidencia. -->

## Checklist

- [ ] Commits en Conventional Commits (tipo en inglés, descripción en español)
- [ ] `ruff check .` y `ruff format --check .` en verde
- [ ] Escenarios con `@tc-*`, prioridad (`@smoke`/`@regression`) y `@negative` cuando aplique
- [ ] Datos y valores esperados en `data/` (YAML); pasos sin literales de negocio ni URLs
- [ ] Bugs del sistema bajo prueba como `@known-bug @bug:<ID>` con su entrada en `data/comun/bugs_conocidos.yaml`
- [ ] Sin secretos: los valores reales van en `.env` o en los secrets del repositorio
