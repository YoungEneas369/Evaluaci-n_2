from dao.dao import DAO
from dao.cliente_dao import ClienteDAO
from dao.paquete_dao import PaqueteDAO
from model.detalle_reserva import DetalleReserva
from model.pago import Pago
from model.reserva import Reserva
from model.viajero import Viajero


class ReservaDAO(DAO):
    def insertar(self, reserva):
        reserva.id = self.ejecutar('''INSERT INTO reservas
            (cliente_id, paquete_id, fecha, precio_unitario, agente_id, estado, cotizacion_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (reserva.cliente.id, reserva.paquete.id, reserva.fecha, reserva.precio_unitario,
             reserva.agente_id, reserva.estado, reserva.cotizacion_id)).lastrowid
        for viajero in reserva.viajeros:
            self.ejecutar('INSERT INTO viajeros(reserva_id, nombre, pasaporte) VALUES (?, ?, ?)',
                          (reserva.id, viajero.nombre, viajero.pasaporte))
        for detalle in reserva.detalles:
            self.ejecutar('''INSERT INTO detalles_reserva(reserva_id, tipo, descripcion, cantidad)
                VALUES (?, ?, ?, ?)''', (reserva.id, detalle.tipo, detalle.descripcion, detalle.cantidad))

    def buscar(self, id):
        f = self.ejecutar('SELECT * FROM reservas WHERE id = ?', (id,)).fetchone()
        if not f:
            return None
        viajeros = [Viajero(v['nombre'], v['pasaporte']) for v in self.ejecutar(
            'SELECT * FROM viajeros WHERE reserva_id = ? ORDER BY id', (id,)).fetchall()]
        detalles = [DetalleReserva(d['tipo'], d['descripcion'], d['cantidad']) for d in self.ejecutar(
            'SELECT * FROM detalles_reserva WHERE reserva_id = ? ORDER BY id', (id,)).fetchall()]
        pagos = [Pago(p['monto'], p['administrador_id'], p['fecha']) for p in self.ejecutar(
            'SELECT * FROM pagos WHERE reserva_id = ? ORDER BY id', (id,)).fetchall()]
        return Reserva(ClienteDAO(self.conexion).buscar(f['cliente_id']),
                       PaqueteDAO(self.conexion).buscar(f['paquete_id']), f['fecha'], viajeros,
                       detalles, f['precio_unitario'], f['agente_id'], f['id'], f['estado'],
                       pagos, f['cotizacion_id'])

    def listar(self):
        ids = self.ejecutar('SELECT id FROM reservas ORDER BY id').fetchall()
        return [self.buscar(f['id']) for f in ids]

    def actualizar_estado(self, reserva):
        self.ejecutar('UPDATE reservas SET estado = ? WHERE id = ?', (reserva.estado, reserva.id))

    def insertar_pago(self, reserva_id, pago):
        self.ejecutar('INSERT INTO pagos(reserva_id, monto, administrador_id, fecha) VALUES (?, ?, ?, ?)',
                      (reserva_id, pago.monto, pago.administrador_id, pago.fecha))
