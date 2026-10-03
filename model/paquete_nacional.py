from model.paquete import Paquete
from validaciones import pesos


class PaqueteNacional(Paquete):
    @property
    def tipo(self):
        return 'nacional'

    @property
    def moneda(self):
        return 'CLP'

    @property
    def requiere_cambio(self):
        return False

    def calcular_precio(self, dolar=None):
        return pesos(self.precio_base)
