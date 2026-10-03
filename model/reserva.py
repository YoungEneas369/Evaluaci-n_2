from excepciones import AnticipoInsuficienteError, DatosInvalidosError, OperacionNoPermitidaError
from validaciones import entero, fecha_iso


class Reserva:
    def __init__(self, cliente, paquete, fecha, viajeros, detalles, precio_unitario,
                 agente_id, id=None, estado='pendiente', pagos=(), cotizacion_id=None):
        if not viajeros or not detalles:
            raise DatosInvalidosError('La reserva necesita viajeros y al menos un detalle.')
        if estado not in ('pendiente', 'confirmada', 'cancelada'):
            raise DatosInvalidosError('Estado de reserva inválido.')
        self.__id = id
        self.__cliente = cliente
        self.__paquete = paquete
        self.__fecha = fecha_iso(fecha)
        self.__viajeros = tuple(viajeros)
        self.__detalles = tuple(detalles)
        self.__precio_unitario = entero(precio_unitario, 'Precio por viajero')
        self.__agente_id = agente_id
        self.__estado = estado
        self.__pagos = list(pagos)
        self.__cotizacion_id = cotizacion_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def cliente(self):
        return self.__cliente

    @property
    def paquete(self):
        return self.__paquete

    @property
    def fecha(self):
        return self.__fecha

    @property
    def viajeros(self):
        return self.__viajeros

    @property
    def detalles(self):
        return self.__detalles

    @property
    def precio_unitario(self):
        return self.__precio_unitario

    @property
    def total(self):
        return self.__precio_unitario * len(self.__viajeros)

    @property
    def agente_id(self):
        return self.__agente_id

    @property
    def estado(self):
        return self.__estado

    @property
    def pagos(self):
        return tuple(self.__pagos)

    @property
    def pagado(self):
        return sum(pago.monto for pago in self.__pagos)

    @property
    def cotizacion_id(self):
        return self.__cotizacion_id

    def registrar_pago(self, pago):
        if self.__estado == 'cancelada':
            raise OperacionNoPermitidaError('Una reserva cancelada no admite pagos.')
        if self.pagado + pago.monto > self.total:
            raise DatosInvalidosError('El pago supera el saldo pendiente.')
        self.__pagos.append(pago)

    def confirmar(self):
        if self.__estado != 'pendiente':
            raise OperacionNoPermitidaError('Solo se puede confirmar una reserva pendiente.')
        if self.__paquete.requiere_pasaporte:
            for viajero in self.__viajeros:
                viajero.validar_pasaporte()
        if self.pagado * 2 < self.total:
            raise AnticipoInsuficienteError('Se necesita al menos el 50 % del total como anticipo.')
        self.__estado = 'confirmada'

    def cancelar(self):
        if self.__estado == 'cancelada':
            raise OperacionNoPermitidaError('La reserva ya está cancelada.')
        if self.pagado:
            raise OperacionNoPermitidaError('La cancelación con pagos requiere gestionar una devolución; queda fuera de esta versión.')
        self.__estado = 'cancelada'
