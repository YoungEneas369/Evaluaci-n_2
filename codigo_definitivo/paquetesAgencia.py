# Representa un paquete nacional con precio por viajero en pesos chilenos.
class PaqueteNacional:
    def __init__(self, nombre_recibido: str, precio_por_viajero_recibido: float):
        self.__nombre = nombre_recibido
        self.__precio_por_viajero = precio_por_viajero_recibido

    # Calcula el total a pagar por un número de viajeros dado.
    def calcular_total(self, cantidad_viajeros: int) -> float:
        return cantidad_viajeros * self.__precio_por_viajero

    # Propiedades de lectura: se consultan sin paréntesis desde fuera de la clase.
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def precio_por_viajero(self) -> float:
        return self.__precio_por_viajero
