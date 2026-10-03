"""Datos ficticios para evaluar la aplicación desde su primer inicio."""
from datetime import date, timedelta

from dao.cliente_dao import ClienteDAO
from dao.disponibilidad_dao import DisponibilidadDAO
from dao.paquete_dao import PaqueteDAO
from dao.proveedor_dao import ProveedorDAO
from dao.usuario_dao import UsuarioDAO
from model.cliente import Cliente
from model.crucero import Crucero
from model.paquete_internacional import PaqueteInternacional
from model.paquete_nacional import PaqueteNacional
from model.proveedor import Proveedor
from servicios.autenticacion import Autenticacion


def cargar_demo(conexion):
    if UsuarioDAO(conexion).cantidad():
        return False
    with conexion:
        auth = Autenticacion(conexion)
        auth.crear_usuario('agente', 'Agente de demostración', 'agente', 'AgenteRutaSur1!')
        auth.crear_usuario('admin', 'Administrador de demostración', 'administrador', 'AdminRutaSur1!')
        proveedor = Proveedor('Operador turístico RutaSur (demo)')
        ProveedorDAO(conexion).insertar(proveedor)
        ClienteDAO(conexion).insertar(Cliente('Cliente de demostración', 'cliente@example.com'))
        paquetes = PaqueteDAO(conexion)
        paquetes.insertar(PaqueteNacional('Chiloé 3 días', '300000', proveedor))
        paquetes.insertar(PaqueteInternacional('Buenos Aires 4 días', '500', proveedor))
        paquetes.insertar(Crucero('Crucero Patagonia', '1000', proveedor))
        fecha = (date.today() + timedelta(days=30)).isoformat()
        DisponibilidadDAO(conexion).establecer_total(proveedor.id, fecha, 20)
    return True
