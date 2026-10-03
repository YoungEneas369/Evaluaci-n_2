import re

from excepciones import PasaporteInvalidoError
from model.persona import Persona


class Viajero(Persona):
    def __init__(self, nombre, pasaporte=''):
        super().__init__(nombre)
        self.__pasaporte = str(pasaporte or '').strip().upper()

    @property
    def pasaporte(self):
        return self.__pasaporte

    def validar_pasaporte(self):
        # Regla académica asumida; no comprueba identidad ni vigencia oficial.
        if not re.fullmatch(r'[A-Z0-9]{6,12}', self.__pasaporte):
            raise PasaporteInvalidoError(
                f'Pasaporte de {self.nombre}: ingrese entre 6 y 12 letras o números.'
            )
        return True
