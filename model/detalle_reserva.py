from excepciones import DatosInvalidosError
from validaciones import entero, texto


class DetalleReserva:
    TIPOS = ('vuelo', 'hotel', 'seguro', 'excursion')

    def __init__(self, tipo, descripcion, cantidad=1):
        if tipo not in self.TIPOS:
            raise DatosInvalidosError('Tipo de ítem desconocido.')
        self.__tipo = tipo
        self.__descripcion = texto(descripcion, 'Descripción del ítem')
        self.__cantidad = entero(cantidad, 'Cantidad del ítem')

    @property
    def tipo(self):
        return self.__tipo

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def cantidad(self):
        return self.__cantidad
