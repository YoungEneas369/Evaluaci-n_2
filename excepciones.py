"""Errores que representan operaciones rechazadas por RutaSur."""


class ErrorAgencia(Exception):
    """La interfaz captura estos errores y permite continuar."""


class DatosInvalidosError(ErrorAgencia):
    pass


class SinCuposError(ErrorAgencia):
    pass


class AnticipoInsuficienteError(ErrorAgencia):
    pass


class PasaporteInvalidoError(DatosInvalidosError):
    pass


class IndicadorNoDisponibleError(ErrorAgencia):
    pass


class OperacionNoPermitidaError(ErrorAgencia):
    pass


class RegistroNoEncontradoError(ErrorAgencia):
    pass
