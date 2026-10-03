from datetime import datetime

from excepciones import DatosInvalidosError
from validaciones import numero_decimal


class TipoCambio:
    def __init__(self, valor, fecha):
        self.__valor = numero_decimal(valor, 'Tipo de cambio')
        try:
            self.__fecha = datetime.fromisoformat(fecha.replace('Z', '+00:00')).isoformat()
        except (ValueError, TypeError, AttributeError):
            raise DatosInvalidosError('Fecha del indicador inválida.') from None

    @property
    def valor(self):
        return self.__valor

    @property
    def fecha(self):
        return self.__fecha
