# Quien viaja puede ser distinto del comprador. No se exige RUT a todo viajero.
class Viajero:
    def __init__(self, nombre_recibido: str, pasaporte: str | None = None):
        if not isinstance(nombre_recibido, str) or not nombre_recibido.strip():
            raise ValueError("El viajero necesita un nombre.")
        self.__nombre = nombre_recibido.strip()
        self.pasaporte = pasaporte

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def pasaporte(self) -> str | None:
        return self.__pasaporte

    @pasaporte.setter
    def pasaporte(self, valor: str | None):
        if valor is None:
            self.__pasaporte = None
            return
        if not isinstance(valor, str):
            raise ValueError("El pasaporte debe ser texto.")
        # Vacío y espacios representan ausencia; nacional puede no exigirlo.
        self.__pasaporte = valor.strip().upper() or None

    def validar_pasaporte(self) -> None:
        # La futura confirmación internacional deberá llamar a esta validación.
        # No se impone una longitud oficial no especificada por el guion.
        if self.__pasaporte is None:
            raise ValueError("El viajero necesita pasaporte para un viaje internacional.")
