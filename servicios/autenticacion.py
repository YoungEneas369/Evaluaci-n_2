import hashlib
import hmac
import secrets

from dao.usuario_dao import UsuarioDAO


class Autenticacion:
    ITERACIONES = 600_000

    def __init__(self, conexion):
        self.__dao = UsuarioDAO(conexion)

    @classmethod
    def _hash(cls, password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                   bytes.fromhex(salt), cls.ITERACIONES).hex()

    def crear_usuario(self, nombre_usuario, nombre, rol, password):
        salt = secrets.token_hex(16)
        return self.__dao.insertar(nombre_usuario, nombre, rol, self._hash(password, salt), salt)

    def iniciar_sesion(self, nombre_usuario, password):
        fila = self.__dao.credenciales(nombre_usuario.strip())
        if fila and hmac.compare_digest(self._hash(password, fila['salt']), fila['hash_password']):
            return self.__dao.crear_objeto(fila)
        return None
