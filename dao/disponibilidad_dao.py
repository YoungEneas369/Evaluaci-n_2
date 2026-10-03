from dao.dao import DAO
from excepciones import DatosInvalidosError, SinCuposError
from model.disponibilidad import Disponibilidad


class DisponibilidadDAO(DAO):
    def buscar(self, proveedor_id, fecha):
        f = self.ejecutar('SELECT * FROM disponibilidad WHERE proveedor_id = ? AND fecha = ?',
                         (proveedor_id, fecha)).fetchone()
        return Disponibilidad(f['proveedor_id'], f['fecha'], f['cupos_totales'], f['cupos_disponibles']) if f else None

    def listar(self):
        return [Disponibilidad(f['proveedor_id'], f['fecha'], f['cupos_totales'], f['cupos_disponibles'])
                for f in self.ejecutar('SELECT * FROM disponibilidad ORDER BY fecha, proveedor_id').fetchall()]

    def establecer_total(self, proveedor_id, fecha, total):
        anterior = self.buscar(proveedor_id, fecha)
        ocupados = anterior.cupos_totales - anterior.cupos_disponibles if anterior else 0
        if total < ocupados:
            raise DatosInvalidosError('El total no puede ser menor que los cupos ya reservados.')
        self.ejecutar('''INSERT INTO disponibilidad VALUES (?, ?, ?, ?)
            ON CONFLICT(proveedor_id, fecha) DO UPDATE SET
            cupos_totales = excluded.cupos_totales, cupos_disponibles = excluded.cupos_disponibles''',
                     (proveedor_id, fecha, total, total - ocupados))

    def ocupar(self, proveedor_id, fecha, cantidad):
        cursor = self.ejecutar('''UPDATE disponibilidad SET cupos_disponibles = cupos_disponibles - ?
            WHERE proveedor_id = ? AND fecha = ? AND cupos_disponibles >= ?''',
                               (cantidad, proveedor_id, fecha, cantidad))
        if cursor.rowcount != 1:
            raise SinCuposError('El proveedor no tiene cupos suficientes para esa fecha.')

    def liberar(self, proveedor_id, fecha, cantidad):
        self.ejecutar('''UPDATE disponibilidad SET cupos_disponibles = cupos_disponibles + ?
            WHERE proveedor_id = ? AND fecha = ?''', (cantidad, proveedor_id, fecha))
