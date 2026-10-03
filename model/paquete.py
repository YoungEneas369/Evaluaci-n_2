from abc import ABC, abstractmethod

from validaciones import numero_decimal, texto


class Paquete(ABC):
    def __init__(self, nombre, precio_base, proveedor, id=None):
        self.__nombre = texto(nombre, 'Nombre del paquete')
        self.precio_base = precio_base
        self.__proveedor = proveedor
        self.__id = id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def nombre(self):
        return self.__nombre

    @property
    def proveedor(self):
        return self.__proveedor

    @property
    def precio_base(self):
        return self.__precio_base

    @precio_base.setter
    def precio_base(self, valor):
        self.__precio_base = numero_decimal(valor, 'Precio base')

    @property
    @abstractmethod
    def tipo(self):
        pass

    @property
    def moneda(self):
        return 'USD'

    @property
    def requiere_cambio(self):
        return True

    @property
    def requiere_pasaporte(self):
        return False

    @abstractmethod
    def calcular_precio(self, dolar=None):
        """Precio final por viajero, en pesos enteros; los ítems están incluidos."""
        pass
