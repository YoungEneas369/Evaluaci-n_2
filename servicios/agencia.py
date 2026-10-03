"""Coordina permisos, objetos y transacciones. Los DAO nunca confirman por separado."""
from datetime import datetime, timezone

from dao.cliente_dao import ClienteDAO
from dao.cotizacion_dao import CotizacionDAO
from dao.disponibilidad_dao import DisponibilidadDAO
from dao.paquete_dao import PaqueteDAO
from dao.proveedor_dao import ProveedorDAO
from dao.reserva_dao import ReservaDAO
from excepciones import RegistroNoEncontradoError, SinCuposError
from model.cliente import Cliente
from model.pago import Pago
from model.proveedor import Proveedor
from model.reserva import Reserva
from servicios.cotizador import Cotizador
from servicios.mindicador import Mindicador
from validaciones import entero, fecha_iso


class Agencia:
    def __init__(self, conexion, indicador=None):
        self.__conexion = conexion
        self.__cotizador = Cotizador(indicador or Mindicador())
        self.clientes = ClienteDAO(conexion)
        self.proveedores = ProveedorDAO(conexion)
        self.paquetes = PaqueteDAO(conexion)
        self.disponibilidad = DisponibilidadDAO(conexion)
        self.reservas = ReservaDAO(conexion)
        self.cotizaciones = CotizacionDAO(conexion)

    @staticmethod
    def _encontrado(objeto):
        if objeto is None:
            raise RegistroNoEncontradoError('No se encontró el registro solicitado.')
        return objeto

    def crear_cliente(self, usuario, nombre, correo):
        usuario.exigir_permiso('gestionar_clientes')
        cliente = Cliente(nombre, correo)
        with self.__conexion:
            self.clientes.insertar(cliente)
        return cliente

    def actualizar_cliente(self, usuario, id, nombre, correo):
        usuario.exigir_permiso('gestionar_clientes')
        self._encontrado(self.clientes.buscar(id))
        with self.__conexion:
            self.clientes.actualizar(Cliente(nombre, correo, id))

    def eliminar_cliente(self, usuario, id):
        usuario.exigir_permiso('gestionar_clientes')
        self._encontrado(self.clientes.buscar(id))
        with self.__conexion:
            self.clientes.eliminar(id)

    def crear_proveedor(self, usuario, nombre):
        usuario.exigir_permiso('gestionar_proveedores')
        proveedor = Proveedor(nombre)
        with self.__conexion:
            self.proveedores.insertar(proveedor)
        return proveedor

    def actualizar_proveedor(self, usuario, id, nombre):
        usuario.exigir_permiso('gestionar_proveedores')
        self._encontrado(self.proveedores.buscar(id))
        with self.__conexion:
            self.proveedores.actualizar(Proveedor(nombre, id))

    def eliminar_proveedor(self, usuario, id):
        usuario.exigir_permiso('gestionar_proveedores')
        self._encontrado(self.proveedores.buscar(id))
        with self.__conexion:
            self.proveedores.eliminar(id)

    def crear_paquete(self, usuario, clase, nombre, precio, proveedor_id):
        usuario.exigir_permiso('gestionar_paquetes')
        proveedor = self._encontrado(self.proveedores.buscar(proveedor_id))
        paquete = clase(nombre, precio, proveedor)
        with self.__conexion:
            self.paquetes.insertar(paquete)
        return paquete

    def cambiar_precio(self, usuario, paquete_id, precio):
        usuario.exigir_permiso('gestionar_paquetes')
        paquete = self._encontrado(self.paquetes.buscar(paquete_id))
        paquete.precio_base = precio
        with self.__conexion:
            self.paquetes.actualizar(paquete)

    def eliminar_paquete(self, usuario, paquete_id):
        usuario.exigir_permiso('gestionar_paquetes')
        self._encontrado(self.paquetes.buscar(paquete_id))
        with self.__conexion:
            self.paquetes.eliminar(paquete_id)

    def configurar_cupos(self, usuario, proveedor_id, fecha, total):
        usuario.exigir_permiso('gestionar_proveedores')
        self._encontrado(self.proveedores.buscar(proveedor_id))
        fecha = fecha_iso(fecha)
        total = entero(total, 'Total de cupos', permitir_cero=True)
        with self.__conexion:
            self.__conexion.execute('BEGIN IMMEDIATE')
            self.disponibilidad.establecer_total(proveedor_id, fecha, total)

    def cotizar(self, usuario, paquete_id):
        usuario.exigir_permiso('consultar')
        paquete = self._encontrado(self.paquetes.buscar(paquete_id))
        precio, indicador = self.__cotizador.cotizar(paquete)
        if indicador:
            with self.__conexion:
                self.cotizaciones.insertar(indicador)
        return precio, indicador

    def registrar_reserva(self, usuario, cliente_id, paquete_id, fecha, viajeros, detalles):
        usuario.exigir_permiso('reservar')
        cliente = self._encontrado(self.clientes.buscar(cliente_id))
        paquete = self._encontrado(self.paquetes.buscar(paquete_id))
        fecha = fecha_iso(fecha)
        disponibilidad = self.disponibilidad.buscar(paquete.proveedor.id, fecha)
        if disponibilidad is None:
            raise SinCuposError('No hay disponibilidad registrada para ese proveedor y fecha.')
        disponibilidad.verificar(len(viajeros))
        if paquete.requiere_pasaporte:
            for viajero in viajeros:
                viajero.validar_pasaporte()
        precio, indicador = self.__cotizador.cotizar(paquete)
        # Una sola transacción: cabecera, viajeros, detalles, indicador y cupos.
        with self.__conexion:
            cotizacion_id = self.cotizaciones.insertar(indicador) if indicador else None
            reserva = Reserva(cliente, paquete, fecha, viajeros, detalles, precio,
                              usuario.id, cotizacion_id=cotizacion_id)
            self.disponibilidad.ocupar(paquete.proveedor.id, fecha, len(viajeros))
            self.reservas.insertar(reserva)
        return reserva

    def registrar_pago(self, usuario, reserva_id, monto):
        usuario.exigir_permiso('registrar_pagos')
        with self.__conexion:
            # Bloqueo de escritura antes de leer el saldo compartido.
            self.__conexion.execute('BEGIN IMMEDIATE')
            reserva = self._encontrado(self.reservas.buscar(reserva_id))
            pago = Pago(monto, usuario.id, datetime.now(timezone.utc).isoformat())
            reserva.registrar_pago(pago)
            self.reservas.insertar_pago(reserva_id, pago)

    def confirmar(self, usuario, reserva_id):
        usuario.exigir_permiso('reservar')
        with self.__conexion:
            self.__conexion.execute('BEGIN IMMEDIATE')
            reserva = self._encontrado(self.reservas.buscar(reserva_id))
            reserva.confirmar()
            self.reservas.actualizar_estado(reserva)

    def cancelar(self, usuario, reserva_id):
        usuario.exigir_permiso('reservar')
        with self.__conexion:
            self.__conexion.execute('BEGIN IMMEDIATE')
            reserva = self._encontrado(self.reservas.buscar(reserva_id))
            reserva.cancelar()
            self.reservas.actualizar_estado(reserva)
            self.disponibilidad.liberar(reserva.paquete.proveedor.id, reserva.fecha, len(reserva.viajeros))
