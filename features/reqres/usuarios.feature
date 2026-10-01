# language: es
@reqres @usuarios @requiere_key
Característica: Gestión de usuarios en ReqRes
  Como consumidor de la API de ReqRes
  quiero consultar, dar de alta y mantener usuarios
  para integrarlos en mi aplicación

  @contrato @tc-api-001 @tc-api-002 @tc-api-007
  Esquema del escenario: Listar usuarios por página respeta la paginación y el contrato
    Dado el caso de prueba "<caso>"
    Cuando consulto el listado de usuarios del caso
    Entonces la respuesta cumple lo esperado del caso

    @smoke
    Ejemplos: Primera página
      | caso                            |
      | reqres.usuarios.listar_pagina_1 |

    @regression
    Ejemplos: Segunda página
      | caso                            |
      | reqres.usuarios.listar_pagina_2 |

  @smoke @contrato @tc-api-012 @tc-api-013
  Escenario: Consultar un usuario existente devuelve sus datos completos
    Dado el caso de prueba "reqres.usuarios.consultar_existente"
    Cuando consulto el usuario del caso
    Entonces la respuesta cumple lo esperado del caso

  @smoke @negative @tc-api-015
  Escenario: Consultar un usuario inexistente devuelve 404
    Dado el caso de prueba "reqres.usuarios.consultar_inexistente"
    Cuando consulto el usuario del caso
    Entonces la respuesta cumple lo esperado del caso

  @smoke @contrato @tc-api-018 @tc-api-023
  Escenario: Crear un usuario con nombre y trabajo
    Dado el caso de prueba "reqres.usuarios.crear_basico"
    Cuando creo el usuario del caso
    Entonces la respuesta cumple lo esperado del caso

  @regression @tc-api-021
  Escenario: Crear un usuario con campos adicionales conserva sus valores y tipos
    Dado el caso de prueba "reqres.usuarios.crear_con_campos_extra"
    Cuando creo el usuario del caso
    Entonces la respuesta cumple lo esperado del caso
