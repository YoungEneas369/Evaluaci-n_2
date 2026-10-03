from dao.dao import DAO
from model.cliente import Cliente


class ClienteDAO(DAO):
    def insertar(self, cliente):
        cliente.id = self.ejecutar('INSERT INTO clientes(nombre, correo) VALUES (?, ?)',
                                  (cliente.nombre, cliente.correo)).lastrowid

    def buscar(self, id):
        fila = self.ejecutar('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
        return Cliente(fila['nombre'], fila['correo'], fila['id']) if fila else None

    def listar(self):
        return [Cliente(f['nombre'], f['correo'], f['id'])
                for f in self.ejecutar('SELECT * FROM clientes ORDER BY id').fetchall()]

    def actualizar(self, cliente):
        return self.ejecutar('UPDATE clientes SET nombre = ?, correo = ? WHERE id = ?',
                            (cliente.nombre, cliente.correo, cliente.id)).rowcount > 0

    def eliminar(self, id):
        return self.ejecutar('DELETE FROM clientes WHERE id = ?', (id,)).rowcount > 0
