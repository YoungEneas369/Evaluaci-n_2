from persona import Persona


# Comprador: conserva contacto, pero el pasaporte pertenece a Viajero.
class Cliente(Persona):
    def __init__(self, nombre_recibido: str, rut_recibido: str,
                 correo_recibido: str, telefono_recibido: str):
        super().__init__(nombre_recibido, rut_recibido)
        self.__correo = correo_recibido
        self.__telefono = telefono_recibido

    def cambiar_nombre(self, nombre_nuevo: str) -> None:
        # Usa el setter heredado y su validación.
        self.nombre = nombre_nuevo

    def cambiar_correo(self, correo_nuevo: str) -> None:
        self.__correo = correo_nuevo

    def cambiar_telefono(self, telefono_nuevo: str) -> None:
        self.__telefono = telefono_nuevo

    @property
    def correo(self) -> str:
        return self.__correo

    @property
    def telefono(self) -> str:
        return self.__telefono
