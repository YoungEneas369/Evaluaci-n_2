from paquetesAgencia import Paquete


class PaqueteInternacional(Paquete):
    # Precio por viajero en USD; tipo_cambio expresa CLP por cada USD.
    def calcular_total(self, cantidad_viajeros: int, tipo_cambio=None) -> float:
        # Evita mostrar un total en pesos si no recibimos una cotización válida.
        if tipo_cambio is None or tipo_cambio <= 0:
            raise ValueError("El paquete internacional necesita un tipo de cambio positivo.")
        return cantidad_viajeros * self.precio_por_viajero * tipo_cambio

#Explicación: La clase PaqueteInternacional hereda de la clase Paquete.
#luego define su propio método calcular_total,
# que multiplica la cantidad de viajeros por el precio por viajero y por el tipo de cambio.
#qué significa tipo_cambio=None: significa que el argumento tipo_cambio es opcional
# y su valor predeterminado es None.
#Se lee: "Si no se proporciona un valor para tipo_cambio, se usará None como valor predeterminado".
#None es un valor especial en Python que representa la ausencia de un valor o un valor nulo.

#en return cantidad_viajeros * self.precio_por_viajero * tipo_cambio,
#  self.precio_por_viajero es una propiedad heredada de la clase Paquete,
# que devuelve el valor del atributo privado __precio_por_viajero.
