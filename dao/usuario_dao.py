from dao.dao import DAO
from model.administrador import Administrador
from model.agente_viajes import AgenteViajes
from model.usuario import Usuario


class UsuarioDAO(DAO):
    def insertar(self, nombre_usuario, nombre, rol, hash_password, salt):
        return self.ejecutar('''INSERT INTO usuarios(nombre_usuario, nombre, rol, hash_password, salt)
            VALUES (?, ?, ?, ?, ?)''', (nombre_usuario, nombre, rol, hash_password, salt)).lastrowid

    def credenciales(self, nombre_usuario):
        return self.ejecutar('SELECT * FROM usuarios WHERE nombre_usuario = ?', (nombre_usuario,)).fetchone()

    def cantidad(self):
        return self.ejecutar('SELECT COUNT(*) FROM usuarios').fetchone()[0]

    def crear_objeto(self, fila):
        clase = AgenteViajes if fila['rol'] == 'agente' else Administrador
        return Usuario(fila['id'], fila['nombre_usuario'], clase(fila['nombre']))
