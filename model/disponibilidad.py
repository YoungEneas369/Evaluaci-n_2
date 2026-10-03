from excepciones import DatosInvalidosError, SinCuposError
from validaciones import entero, fecha_iso


class Disponibilidad:
    def __init__(self, proveedor_id, fecha, cupos_totales, cupos_disponibles):
        self.__proveedor_id = proveedor_id
        self.__fecha = fecha_iso(fecha)
        self.__total = entero(cupos_totales, 'Cupos totales', permitir_cero=True)
        self.__disponibles = entero(cupos_disponibles, 'Cupos disponibles', permitir_cero=True)
        if self.__disponibles > self.__total:
            raise DatosInvalidosError('Los cupos disponibles no pueden superar el total.')

    @property
    def proveedor_id(self):
        return self.__proveedor_id

    @property
    def fecha(self):
        return self.__fecha

    @property
    def cupos_totales(self):
        return self.__total

    @property
    def cupos_disponibles(self):
        return self.__disponibles

    def verificar(self, cantidad):
        if entero(cantidad, 'Viajeros') > self.__disponibles:
            raise SinCuposError('El proveedor no tiene cupos suficientes para esa fecha.')
