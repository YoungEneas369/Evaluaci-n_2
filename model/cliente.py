from model.persona import Persona
from validaciones import texto


class Cliente(Persona):
    """La persona que compra puede ser distinta de quienes viajan."""
    def __init__(self, nombre, correo, id=None):
        super().__init__(nombre)
        self.__correo = texto(correo, 'Correo')
        self.__id = id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def correo(self):
        return self.__correo
