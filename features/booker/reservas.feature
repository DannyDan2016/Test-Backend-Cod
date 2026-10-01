# language: es
@booker @reservas
Característica: Ciclo de vida de una reserva en restful-booker
  Como cliente de la API de reservas
  quiero crear, consultar, modificar y cancelar reservas
  para gestionar mis estancias

  Antecedentes:
    Dado que restful-booker está disponible
    Y que dispongo de un token de autenticación válido

  @smoke @contrato @tc-api-225
  Escenario: Ciclo de vida completo de una reserva autenticada con token
    Cuando creo una reserva según el caso "booker.reservas.crear"
    Entonces la respuesta cumple lo esperado del caso
    Cuando consulto la reserva creada según el caso "booker.reservas.consultar"
    Entonces la respuesta cumple lo esperado del caso
    Cuando actualizo la reserva creada con el token según el caso "booker.reservas.actualizar"
    Entonces la respuesta cumple lo esperado del caso
    Cuando consulto la reserva creada según el caso "booker.reservas.consultar"
    Entonces la respuesta cumple lo esperado del caso
    Cuando borro la reserva creada con el token según el caso "booker.reservas.borrar"
    Entonces la respuesta cumple lo esperado del caso
    Cuando consulto la reserva creada según el caso "booker.reservas.consultar_borrada"
    Entonces la respuesta cumple lo esperado del caso

  @regression @known-bug @bug:BKR-BUG-6 @tc-api-203
  Escenario: Crear una reserva responde 201 Created
    Cuando creo una reserva según el caso "booker.reservas.crear_responde_201"
    Entonces la respuesta cumple lo esperado del caso

  @regression @known-bug @bug:BKR-BUG-3 @tc-api-216
  Escenario: Borrar una reserva responde sin indicar una creación
    Dado una reserva creada según el caso "booker.reservas.crear"
    Cuando borro la reserva creada con el token según el caso "booker.reservas.borrar_responde_sin_contenido"
    Entonces la respuesta cumple lo esperado del caso
