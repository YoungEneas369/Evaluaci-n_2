from decimal import Decimal

from model.paquete import Paquete
from validaciones import numero_decimal, pesos


class Crucero(Paquete):
    RECARGO_SERVICIO = Decimal('0.10')  # Supuesto documentado del equipo.

    @property
    def tipo(self):
        return 'crucero'

    def calcular_precio(self, dolar=None):
        convertido = self.precio_base * numero_decimal(dolar, 'Valor del dólar')
        return pesos(convertido * (1 + self.RECARGO_SERVICIO))
