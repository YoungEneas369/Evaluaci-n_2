from validaciones import texto


class Proveedor:
    def __init__(self, nombre, id=None):
        self.__nombre = texto(nombre, 'Proveedor')
        self.__id = id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor
