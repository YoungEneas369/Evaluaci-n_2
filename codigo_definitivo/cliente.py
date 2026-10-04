class Cliente: #Aquí creamos la clase cliente, tendrá atributos que son como sus características. entonces vamos poniendo de que tipo será su valor.
#Un Cliente tiene nombre, correo y telefono :3-
    __nombre: str #Valor string (candena de texto)
    __correo: str #Valor string (candena de texto)
    __telefono: str #puede incluir un +, y ceros iniciales y esto no lo ocuparemos para cálculos.
# Sacamos pass porque la clase ya tiene declaraciones de atributos.

    # Inicializa los datos de cada cliente al crear el objeto.
    def __init__(self, nombre_recibido: str, correo_recibido: str, telefono_recibido: str):
        self.__nombre = nombre_recibido      # Guarda el nombre recibido en este cliente.
        self.__correo = correo_recibido      # Guarda el correo recibido en este cliente.
        self.__telefono = telefono_recibido  # Guarda el teléfono recibido en este cliente.

    # Reemplaza el correo guardado en el cliente que llama al método.
    def cambiar_correo(self, correo_nuevo: str) -> None:
        self.__correo = correo_nuevo

    # Reemplaza el teléfono guardado en el cliente que llama al método.
    def cambiar_telefono(self, telefono_nuevo: str) -> None:
        self.__telefono = telefono_nuevo

    def cambiar_nombre(self, nombre_nuevo: str) -> None:
        self.__nombre = nombre_nuevo

    # -> None indica que el método no retorna un resultado útil.
    # Estas propiedades permiten leer los atributos privados sin usar paréntesis.
    # El prefijo __ hace que Python cambie internamente el nombre del atributo 
    # para evitar accesos accidentales desde fuera de la clase. 
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def correo(self) -> str:
        return self.__correo

    @property
    def telefono(self) -> str:
        return self.__telefono


