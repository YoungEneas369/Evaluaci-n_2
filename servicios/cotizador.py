class Cotizador:
    def __init__(self, indicador):
        self.__indicador = indicador

    def cotizar(self, paquete):
        indicador = self.__indicador.obtener_dolar() if paquete.requiere_cambio else None
        # La misma llamada sirve para los tres subtipos: polimorfismo.
        precio = paquete.calcular_precio(indicador.valor if indicador else None)
        return precio, indicador
