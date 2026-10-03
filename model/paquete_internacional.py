from model.paquete import Paquete
from validaciones import numero_decimal, pesos


class PaqueteInternacional(Paquete):
    @property
    def tipo(self):
        return 'internacional'

    @property
    def requiere_pasaporte(self):
        return True

    def calcular_precio(self, dolar=None):
        return pesos(self.precio_base * numero_decimal(dolar, 'Valor del dólar'))
