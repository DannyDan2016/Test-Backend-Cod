# language: es
@reqres @robustez @requiere_key
Característica: Seguridad y robustez de la API de ReqRes
  Como consumidor de la API de ReqRes
  quiero que las peticiones inválidas se rechacen con errores claros y que los retardos sean acotados
  para poder diagnosticar los fallos y fijar timeouts fiables

  @smoke @negative @seguridad @contrato @tc-api-052
  Escenario: Rechazar una petición con una api key no reconocida
    Dado el caso de prueba "reqres.robustez.api_key_invalida"
    Cuando consulto el usuario del caso con la api key del caso
    Entonces la respuesta cumple lo esperado del caso

  @smoke @negative @contrato @tc-api-019
  Escenario: Rechazar el alta de un usuario con JSON malformado
    Dado el caso de prueba "reqres.robustez.json_malformado"
    Cuando envío el cuerpo crudo del caso al alta de usuarios
    Entonces la respuesta cumple lo esperado del caso

  @regression @rendimiento @tc-api-009
  Escenario: Una respuesta con retardo llega dentro del umbral del ambiente
    Dado el caso de prueba "reqres.robustez.respuesta_con_retardo"
    Cuando consulto el listado de usuarios con el retardo del caso
    Entonces la respuesta cumple lo esperado del caso
