from abc import ABC, abstractmethod

from model.persona import Persona


class Trabajador(Persona, ABC):
    @property
    @abstractmethod
    def rol(self):
        pass

    @abstractmethod
    def puede(self, accion):
        pass
