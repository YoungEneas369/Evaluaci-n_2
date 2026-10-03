"""Interfaz de consola. Las reglas de negocio viven en los modelos y servicios."""
import argparse
from getpass import getpass
from sqlite3 import DatabaseError, IntegrityError

from conectar import crear_conexion
from dao.esquema import crear_tablas
from datos_demo import cargar_demo
from excepciones import DatosInvalidosError, ErrorAgencia, RegistroNoEncontradoError
from model.crucero import Crucero
from model.detalle_reserva import DetalleReserva
from model.paquete_internacional import PaqueteInternacional
from model.paquete_nacional import PaqueteNacional
from model.viajero import Viajero
from servicios.agencia import Agencia
from servicios.autenticacion import Autenticacion
from validaciones import entero


def clp(valor):
    return '$' + format(valor, ',').replace(',', '.') + ' CLP'


def pedir_id(mensaje='ID: '):
    return entero(input(mensaje), 'ID')


class Consola:
    def __init__(self, agencia, usuario):
        self.agencia = agencia
        self.usuario = usuario

    def paquetes(self):
        registros = self.agencia.paquetes.listar()
        if not registros:
            print('No hay paquetes registrados.')
        for p in registros:
            print(f'{p.id} | {p.nombre} | {p.tipo} | Base: {p.precio_base} {p.moneda} por viajero | Proveedor: {p.proveedor.id}')

    def proveedores(self):
        for p in self.agencia.proveedores.listar():
            print(f'{p.id} | {p.nombre}')
        for d in self.agencia.disponibilidad.listar():
            print(f'Proveedor {d.proveedor_id} | Fecha {d.fecha} | Cupos {d.cupos_disponibles}/{d.cupos_totales}')

    def clientes(self):
        for c in self.agencia.clientes.listar():
            print(f'{c.id} | {c.nombre} | {c.correo}')

    def cotizar(self):
        self.paquetes()
        precio, indicador = self.agencia.cotizar(self.usuario, pedir_id('ID del paquete: '))
        print(f'Precio final por viajero: {clp(precio)} (ítems incluidos).')
        if indicador:
            print(f'Dólar observado: {indicador.valor} CLP/USD. Fecha publicada: {indicador.fecha}')

    def crear_paquete(self):
        clases = {'1': PaqueteNacional, '2': PaqueteInternacional, '3': Crucero}
        tipo = input('Tipo: 1 nacional, 2 internacional, 3 crucero: ').strip()
        if tipo not in clases:
            raise DatosInvalidosError('Tipo de paquete inválido.')
        nombre = input('Nombre: ')
        precio = input('Precio base por viajero (CLP nacional / USD otros; sin separador de miles): ')
        self.proveedores()
        p = self.agencia.crear_paquete(self.usuario, clases[tipo], nombre, precio, pedir_id('Proveedor ID: '))
        print(f'Paquete creado con ID {p.id}.')

    def cambiar_precio(self):
        self.paquetes()
        id = pedir_id('Paquete ID: ')
        self.agencia.cambiar_precio(self.usuario, id, input('Nuevo precio base: '))
        print('Precio actualizado.')

    def eliminar_paquete(self):
        self.paquetes()
        id = pedir_id('Paquete ID a eliminar: ')
        if input('Escriba SI para eliminar: ').strip().upper() == 'SI':
            self.agencia.eliminar_paquete(self.usuario, id)
            print('Paquete eliminado.')

    def crear_cliente(self):
        c = self.agencia.crear_cliente(self.usuario, input('Nombre del cliente: '), input('Correo: '))
        print(f'Cliente creado con ID {c.id}.')

    def actualizar_cliente(self):
        self.clientes()
        self.agencia.actualizar_cliente(self.usuario, pedir_id(), input('Nuevo nombre: '), input('Nuevo correo: '))
        print('Cliente actualizado.')

    def eliminar_cliente(self):
        self.clientes()
        id = pedir_id()
        if input('Escriba SI para eliminar: ').strip().upper() == 'SI':
            self.agencia.eliminar_cliente(self.usuario, id)
            print('Cliente eliminado.')

    def crear_proveedor(self):
        p = self.agencia.crear_proveedor(self.usuario, input('Nombre del proveedor: '))
        print(f'Proveedor creado con ID {p.id}.')

    def actualizar_proveedor(self):
        self.proveedores()
        self.agencia.actualizar_proveedor(self.usuario, pedir_id(), input('Nuevo nombre: '))
        print('Proveedor actualizado.')

    def eliminar_proveedor(self):
        self.proveedores()
        id = pedir_id()
        if input('Escriba SI para eliminar: ').strip().upper() == 'SI':
            self.agencia.eliminar_proveedor(self.usuario, id)
            print('Proveedor eliminado.')

    def configurar_cupos(self):
        self.proveedores()
        self.agencia.configurar_cupos(self.usuario, pedir_id('Proveedor ID: '),
                                     input('Fecha AAAA-MM-DD: '), input('Total de cupos: '))
        print('Disponibilidad actualizada.')

    def reservar(self):
        self.clientes()
        cliente_id = pedir_id('Cliente comprador ID: ')
        self.paquetes()
        paquete_id = pedir_id('Paquete ID: ')
        paquete = self.agencia.paquetes.buscar(paquete_id)
        if paquete is None:
            raise RegistroNoEncontradoError('No existe ese paquete.')
        self.proveedores()
        fecha = input('Fecha de salida AAAA-MM-DD: ')
        cantidad = entero(input('Cantidad de viajeros: '), 'Cantidad de viajeros')
        viajeros = []
        for n in range(cantidad):
            nombre = input(f'Nombre del viajero {n + 1}: ')
            pasaporte = input('Pasaporte (6 a 12 letras o números): ') if paquete.requiere_pasaporte else ''
            viajero = Viajero(nombre, pasaporte)
            if paquete.requiere_pasaporte:
                viajero.validar_pasaporte()
            viajeros.append(viajero)
        detalles = []
        print('Los detalles ya están incluidos en el precio; no se cobran nuevamente.')
        for tipo in DetalleReserva.TIPOS:
            descripcion = input(f'Descripción de {tipo} (Enter para omitir): ').strip()
            if descripcion:
                detalles.append(DetalleReserva(tipo, descripcion, cantidad))
        r = self.agencia.registrar_reserva(self.usuario, cliente_id, paquete_id, fecha, viajeros, detalles)
        print(f'Reserva {r.id} creada pendiente. Total: {clp(r.total)}. Anticipo mínimo: {clp((r.total + 1) // 2)}.')

    def reservas(self):
        registros = self.agencia.reservas.listar()
        if not registros:
            print('No hay reservas registradas.')
        for r in registros:
            print(f'{r.id} | {r.cliente.nombre} | {r.paquete.nombre} | {r.fecha} | {r.estado} | Total {clp(r.total)} | Pagado {clp(r.pagado)}')

    def detalle(self):
        r = self.agencia.reservas.buscar(pedir_id('Reserva ID: '))
        if r is None:
            raise RegistroNoEncontradoError('No existe esa reserva.')
        print(f'Reserva {r.id}: {r.paquete.nombre}, {r.fecha}, {r.estado}')
        print(f'Comprador: {r.cliente.nombre}. Precio acordado por viajero: {clp(r.precio_unitario)}.')
        for v in r.viajeros:
            print(f'Viajero: {v.nombre} | Pasaporte: {v.pasaporte or "No requerido"}')
        for d in r.detalles:
            print(f'{d.tipo} | {d.descripcion} | Cantidad {d.cantidad} | Incluido')
        for p in r.pagos:
            print(f'Pago: {clp(p.monto)} | {p.fecha}')
        print(f'Total: {clp(r.total)}. Pagado: {clp(r.pagado)}. Saldo: {clp(r.total - r.pagado)}.')

    def pagar(self):
        self.reservas()
        self.agencia.registrar_pago(self.usuario, pedir_id('Reserva ID: '), input('Monto CLP entero: '))
        print('Pago registrado.')

    def confirmar(self):
        self.reservas()
        self.agencia.confirmar(self.usuario, pedir_id('Reserva ID: '))
        print('Reserva confirmada.')

    def cancelar(self):
        self.reservas()
        self.agencia.cancelar(self.usuario, pedir_id('Reserva ID: '))
        print('Reserva cancelada; cupos liberados.')

    def indicadores(self):
        for fila in self.agencia.cotizaciones.listar():
            print(dict(fila))

    def ejecutar(self):
        opciones = {
            '1': ('Listar paquetes', self.paquetes, 'consultar'),
            '2': ('Cotizar precio final', self.cotizar, 'consultar'),
            '3': ('Ver proveedores y cupos', self.proveedores, 'consultar'),
            '4': ('Listar reservas', self.reservas, 'consultar'),
            '5': ('Consultar detalle de reserva', self.detalle, 'consultar'),
            '6': ('Historial del dólar consultado', self.indicadores, 'consultar'),
            '10': ('Crear paquete', self.crear_paquete, 'gestionar_paquetes'),
            '11': ('Modificar precio', self.cambiar_precio, 'gestionar_paquetes'),
            '12': ('Eliminar paquete', self.eliminar_paquete, 'gestionar_paquetes'),
            '13': ('Listar clientes', self.clientes, 'gestionar_clientes'),
            '14': ('Crear cliente', self.crear_cliente, 'gestionar_clientes'),
            '15': ('Modificar cliente', self.actualizar_cliente, 'gestionar_clientes'),
            '16': ('Eliminar cliente', self.eliminar_cliente, 'gestionar_clientes'),
            '17': ('Crear reserva', self.reservar, 'reservar'),
            '18': ('Confirmar reserva (mínimo 50 %)', self.confirmar, 'reservar'),
            '19': ('Cancelar reserva sin pagos', self.cancelar, 'reservar'),
            '20': ('Crear proveedor', self.crear_proveedor, 'gestionar_proveedores'),
            '21': ('Modificar proveedor', self.actualizar_proveedor, 'gestionar_proveedores'),
            '22': ('Eliminar proveedor', self.eliminar_proveedor, 'gestionar_proveedores'),
            '23': ('Configurar cupos por fecha', self.configurar_cupos, 'gestionar_proveedores'),
            '24': ('Registrar pago', self.pagar, 'registrar_pagos'),
        }
        disponibles = {k: v for k, v in opciones.items() if self.usuario.trabajador.puede(v[2])}
        while True:
            print(f'\nRUTASUR | {self.usuario.nombre_usuario} | {self.usuario.trabajador.rol}')
            for k, (nombre, _, _) in disponibles.items():
                print(f'{k}. {nombre}')
            opcion = input('0. Cerrar sesión\nOpción: ').strip()
            if opcion == '0':
                return
            if opcion not in disponibles:
                print('Opción inválida. Seleccione una opción del menú.')
                continue
            try:
                disponibles[opcion][1]()
            except ErrorAgencia as error:
                print(f'No se pudo completar: {error}')
            except IntegrityError:
                print('No se pudo completar: el registro está relacionado con otros datos o incumple una restricción.')
            except DatabaseError:
                print('No se pudo completar la operación de base de datos. Intente nuevamente.')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Agencia de viajes RutaSur')
    parser.add_argument('--db', help='Ruta opcional a una base SQLite de pruebas')
    args = parser.parse_args(argv)
    conexion = None
    try:
        conexion = crear_conexion(args.db)
        crear_tablas(conexion)
        if cargar_demo(conexion):
            print('Datos de demostración creados. Usuarios: agente / AgenteRutaSur1! y admin / AdminRutaSur1!')
        autenticacion = Autenticacion(conexion)
        agencia = Agencia(conexion)
        while True:
            opcion = input('\nRUTASUR\n1. Iniciar sesión\n0. Salir\nOpción: ').strip()
            if opcion == '0':
                break
            if opcion != '1':
                print('Opción inválida.')
                continue
            usuario = autenticacion.iniciar_sesion(input('Usuario: '), getpass('Contraseña: '))
            if usuario is None:
                print('Credenciales incorrectas.')
                continue
            Consola(agencia, usuario).ejecutar()
    except (EOFError, KeyboardInterrupt):
        print('\nSesión finalizada.')
    except DatabaseError as error:
        print(f'No se pudo iniciar o consultar la base de datos: {error}')
    finally:
        if conexion is not None:
            conexion.close()


if __name__ == '__main__':
    main()
