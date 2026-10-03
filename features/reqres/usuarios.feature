# language: es
@reqres @usuarios @requiere_key
Característica: Gestión de usuarios en ReqRes
  Como consumidor de la API de ReqRes
  quiero dar de alta y mantener usuarios
  para integrarlos en mi aplicación

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
