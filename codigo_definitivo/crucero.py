from paquetesAgencia import Paquete


class Crucero(Paquete):
    # Fórmula didáctica: recargo del 10 %, no exigido por el profesor.
    # Precio por viajero en USD. Las noches son informativas en este ejemplo.
    def calcular_total(self, cantidad_viajeros: int, tipo_cambio=None) -> float:
        if tipo_cambio is None or tipo_cambio <= 0:
            raise ValueError("El crucero necesita un tipo de cambio positivo.")
        total_en_pesos = cantidad_viajeros * self.precio_por_viajero * tipo_cambio
        recargo = total_en_pesos * 0.10
        return total_en_pesos + recargo

    # Las noches son un dato elegido para practicar, no una regla del profesor.
    def __init__(self, nombre_recibido: str, precio_por_viajero_recibido: float,noches_recibidas: int):
        # Inicializa nombre y precio en este mismo objeto usando el padre.
        super().__init__(nombre_recibido, precio_por_viajero_recibido)
        #"«Ejecuta el constructor del padre para inicializar el nombre y el precio de este objeto»."
        # Guarda el dato propio del crucero como atributo privado.
        self.__noches = noches_recibidas

        #Al definir un __init__ en la clase hija, se reemplaza el constructor del padre.
        # Por eso usamos super() para llamar al constructor del padre
        # y así inicializar nombre y precio en este mismo objeto y guardarlos en el propio objeto.
        #y añadimos el atributo propio noches con el valor recibido
        # y lo guardamos en el objeto con self.__noches = noches_recibidas.

    # Permite consultar las noches, sin habilitar la asignación directa.
    @property
    def noches(self) -> int:
        return self.__noches
