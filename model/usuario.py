from excepciones import OperacionNoPermitidaError


class Usuario:
    def __init__(self, id, nombre_usuario, trabajador):
        self.__id = id
        self.__nombre_usuario = nombre_usuario
        self.__trabajador = trabajador

    @property
    def id(self):
        return self.__id

    @property
    def nombre_usuario(self):
        return self.__nombre_usuario

    @property
    def trabajador(self):
        return self.__trabajador

    def exigir_permiso(self, accion):
        if not self.__trabajador.puede(accion):
            raise OperacionNoPermitidaError('Su rol no tiene permiso para esta operación.')
