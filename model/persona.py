from validaciones import texto


class Persona:
    def __init__(self, nombre):
        self.__nombre = texto(nombre, 'Nombre')

    @property
    def nombre(self):
        return self.__nombre
