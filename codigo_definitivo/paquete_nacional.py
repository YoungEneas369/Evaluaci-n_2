from paquetesAgencia import Paquete


# Un paquete nacional es un tipo de Paquete.
class PaqueteNacional(Paquete):
    # Precio en CLP. Acepta el mismo parámetro que las otras clases, pero no lo usa.
    def calcular_total(self, cantidad_viajeros: int, tipo_cambio=None) -> float:
        return cantidad_viajeros * self.precio_por_viajero
