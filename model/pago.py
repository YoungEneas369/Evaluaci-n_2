from validaciones import entero


class Pago:
    def __init__(self, monto, administrador_id, fecha):
        self.__monto = entero(monto, 'Monto del pago')
        self.__administrador_id = administrador_id
        self.__fecha = fecha

    @property
    def monto(self):
        return self.__monto

    @property
    def administrador_id(self):
        return self.__administrador_id

    @property
    def fecha(self):
        return self.__fecha
