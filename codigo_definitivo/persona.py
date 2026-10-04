# Adaptado del trabajo de Elías: datos comunes y setters.
class Persona:
    def __init__(self, nombre: str, rut: str):
        # Llama a los setters también al crear el objeto.
        self.nombre = nombre
        self.rut = rut

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        self.__nombre = valor.strip()

    @property
    def rut(self) -> str:
        return self.__rut

    @rut.setter
    def rut(self, valor: str):
        # Solo presencia, no formato ni dígito verificador.
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El RUT no puede estar vacío.")
        self.__rut = valor.strip()
