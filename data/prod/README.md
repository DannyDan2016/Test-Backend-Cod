# Datos del ambiente prod

Sin overrides por ahora: prod usa los valores de `data/comun/`. Añade aquí archivos con la
misma ruta relativa que en `data/comun/` (p. ej. `reqres/usuarios.yaml`) y solo las claves
que cambien; se combinan con un merge profundo en el que gana este ambiente.
