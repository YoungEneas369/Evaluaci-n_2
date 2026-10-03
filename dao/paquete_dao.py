from dao.dao import DAO
from model.proveedor import Proveedor
from model.paquete_nacional import PaqueteNacional
from model.paquete_internacional import PaqueteInternacional
from model.crucero import Crucero


class PaqueteDAO(DAO):
    # Estas sentencias son fijas. Ningún nombre de tabla proviene del usuario.
    INSERTAR_SUBTIPO = {
        'nacional': 'INSERT INTO paquetes_nacionales(paquete_id) VALUES (?)',
        'internacional': 'INSERT INTO paquetes_internacionales(paquete_id) VALUES (?)',
        'crucero': 'INSERT INTO cruceros(paquete_id) VALUES (?)',
    }
    CONSULTA = '''SELECT p.*, pr.nombre AS proveedor_nombre,
        n.paquete_id AS nacional, i.paquete_id AS internacional, c.paquete_id AS crucero
        FROM paquetes p JOIN proveedores pr ON pr.id = p.proveedor_id
        LEFT JOIN paquetes_nacionales n ON n.paquete_id = p.id
        LEFT JOIN paquetes_internacionales i ON i.paquete_id = p.id
        LEFT JOIN cruceros c ON c.paquete_id = p.id'''

    def insertar(self, paquete):
        paquete.id = self.ejecutar(
            'INSERT INTO paquetes(nombre, precio_base, proveedor_id) VALUES (?, ?, ?)',
            (paquete.nombre, str(paquete.precio_base), paquete.proveedor.id)).lastrowid
        self.ejecutar(self.INSERTAR_SUBTIPO[paquete.tipo], (paquete.id,))

    def _objeto(self, fila):
        if not fila:
            return None
        # Aquí se reconstruye el subtipo. El cálculo posterior es polimórfico.
        clase = PaqueteNacional if fila['nacional'] else PaqueteInternacional if fila['internacional'] else Crucero
        proveedor = Proveedor(fila['proveedor_nombre'], fila['proveedor_id'])
        return clase(fila['nombre'], fila['precio_base'], proveedor, fila['id'])

    def buscar(self, id):
        return self._objeto(self.ejecutar(self.CONSULTA + ' WHERE p.id = ?', (id,)).fetchone())

    def listar(self):
        return [self._objeto(f) for f in self.ejecutar(self.CONSULTA + ' ORDER BY p.id').fetchall()]

    def actualizar(self, paquete):
        return self.ejecutar('UPDATE paquetes SET precio_base = ? WHERE id = ?',
                            (str(paquete.precio_base), paquete.id)).rowcount > 0

    def eliminar(self, id):
        # CASCADE elimina el subtipo; una reserva existente impide borrar su paquete.
        return self.ejecutar('DELETE FROM paquetes WHERE id = ?', (id,)).rowcount > 0
