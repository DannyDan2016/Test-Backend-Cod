# language: es
@reqres @robustez @requiere_key
Característica: Robustez de la API de ReqRes ante peticiones inválidas
  Como consumidor de la API de ReqRes
  quiero que las peticiones inválidas se rechacen con errores claros
  para poder diagnosticarlas sin ambigüedad

  @smoke @negative @contrato @tc-api-019
  Escenario: Rechazar el alta de un usuario con JSON malformado
    Dado el caso de prueba "reqres.robustez.json_malformado"
    Cuando envío el cuerpo crudo del caso al alta de usuarios
    Entonces la respuesta cumple lo esperado del caso
