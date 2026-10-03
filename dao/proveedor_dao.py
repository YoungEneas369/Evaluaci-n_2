from dao.dao import DAO
from model.proveedor import Proveedor


class ProveedorDAO(DAO):
    def insertar(self, proveedor):
        proveedor.id = self.ejecutar('INSERT INTO proveedores(nombre) VALUES (?)',
                                    (proveedor.nombre,)).lastrowid

    def buscar(self, id):
        fila = self.ejecutar('SELECT * FROM proveedores WHERE id = ?', (id,)).fetchone()
        return Proveedor(fila['nombre'], fila['id']) if fila else None

    def listar(self):
        return [Proveedor(f['nombre'], f['id'])
                for f in self.ejecutar('SELECT * FROM proveedores ORDER BY id').fetchall()]

    def actualizar(self, proveedor):
        return self.ejecutar('UPDATE proveedores SET nombre = ? WHERE id = ?',
                            (proveedor.nombre, proveedor.id)).rowcount > 0

    def eliminar(self, id):
        return self.ejecutar('DELETE FROM proveedores WHERE id = ?', (id,)).rowcount > 0
