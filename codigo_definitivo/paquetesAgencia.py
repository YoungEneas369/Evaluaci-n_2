# Clase general: reúne los datos que compartirán los tipos de paquete.
# En este ejercicio usamos un precio de ejemplo en pesos chilenos.
class Paquete:
    def __init__(self, nombre_recibido: str, precio_por_viajero_recibido: float):
        self.__nombre = nombre_recibido
        self.__precio_por_viajero = precio_por_viajero_recibido

    # Calcula el total a pagar por un número de viajeros dado.
    def calcular_total(self, cantidad_viajeros: int, tipo_cambio=None) -> float:
        return cantidad_viajeros * self.__precio_por_viajero

    # Propiedades de lectura: se consultan sin paréntesis desde fuera de la clase.
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def precio_por_viajero(self) -> float:
        return self.__precio_por_viajero
