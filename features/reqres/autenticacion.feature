# language: es
@reqres @autenticacion @requiere_key
Característica: Registro e inicio de sesión en ReqRes
  Como usuario de una aplicación que usa ReqRes
  quiero registrarme e iniciar sesión
  para obtener un token con el que acceder a la API

  @contrato @tc-api-039 @tc-api-040 @tc-api-041 @tc-api-043
  Esquema del escenario: Registrar un usuario: <situacion>
    Dado el caso de prueba "<caso>"
    Cuando me registro con los datos del caso
    Entonces la respuesta cumple lo esperado del caso

    @smoke
    Ejemplos: Registro correcto
      | situacion                 | caso                                     |
      | usuario predefinido       | reqres.autenticacion.registro_correcto   |

    @smoke @negative
    Ejemplos: Datos obligatorios
      | situacion                 | caso                                     |
      | sin password              | reqres.autenticacion.registro_sin_password |

    @regression @negative
    Ejemplos: Usuario no permitido
      | situacion                 | caso                                             |
      | usuario no predefinido    | reqres.autenticacion.registro_usuario_no_definido |

  @contrato @tc-api-045 @tc-api-046 @tc-api-047 @tc-api-048
  Esquema del escenario: Iniciar sesión: <situacion>
    Dado el caso de prueba "<caso>"
    Cuando inicio sesión con los datos del caso
    Entonces la respuesta cumple lo esperado del caso

    @smoke
    Ejemplos: Login correcto
      | situacion           | caso                                |
      | usuario predefinido | reqres.autenticacion.login_correcto |

    @smoke @negative
    Ejemplos: Falta la password
      | situacion    | caso                                    |
      | sin password | reqres.autenticacion.login_sin_password |

    @regression @negative
    Ejemplos: Falta el email
      | situacion | caso                                 |
      | sin email | reqres.autenticacion.login_sin_email |

  @regression @negative @known-bug @bug:DEV-004 @tc-api-049
  Escenario: Iniciar sesión con una password incorrecta se rechaza
    Dado el caso de prueba "reqres.autenticacion.login_password_incorrecta"
    Cuando inicio sesión con los datos del caso
    Entonces la respuesta cumple lo esperado del caso
