import io
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from conectar import crear_conexion
from dao.esquema import crear_tablas
from datos_demo import cargar_demo
from excepciones import (AnticipoInsuficienteError, DatosInvalidosError,
                         IndicadorNoDisponibleError, OperacionNoPermitidaError,
                         PasaporteInvalidoError, SinCuposError)
from main import Consola, main
from model.crucero import Crucero
from model.detalle_reserva import DetalleReserva
from model.paquete import Paquete
from model.paquete_internacional import PaqueteInternacional
from model.paquete_nacional import PaqueteNacional
from model.tipo_cambio import TipoCambio
from model.viajero import Viajero
from servicios.agencia import Agencia
from servicios.autenticacion import Autenticacion
from servicios.mindicador import Mindicador


class ProyectoTest(unittest.TestCase):
    FECHA = '2030-01-15'

    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / 'test.db'
        self.con = crear_conexion(self.ruta)
        self.addCleanup(self.con.close)
        crear_tablas(self.con)
        # Aceleración exclusiva de pruebas; producción conserva 600 000 iteraciones.
        self.iteraciones = patch.object(Autenticacion, 'ITERACIONES', 1000)
        self.iteraciones.start()
        self.addCleanup(self.iteraciones.stop)
        cargar_demo(self.con)
        auth = Autenticacion(self.con)
        self.agente = auth.iniciar_sesion('agente', 'AgenteRutaSur1!')
        self.admin = auth.iniciar_sesion('admin', 'AdminRutaSur1!')
        self.indicador = Mock()
        self.indicador.obtener_dolar.return_value = TipoCambio('950', '2026-10-02T00:00:00Z')
        self.app = Agencia(self.con, self.indicador)
        self.app.configurar_cupos(self.admin, 1, self.FECHA, 10)

    def reservar(self, paquete_id=1, pasaporte='', cantidad=1):
        viajeros = [Viajero(f'Viajero {n}', pasaporte) for n in range(cantidad)]
        detalles = [DetalleReserva(tipo, f'Servicio {tipo}', cantidad) for tipo in DetalleReserva.TIPOS]
        return self.app.registrar_reserva(self.agente, 1, paquete_id, self.FECHA, viajeros, detalles)

    def consola(self, entradas, usuario=None):
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas), redirect_stdout(salida):
            Consola(self.app, usuario or self.agente).ejecutar()
        return salida.getvalue()

    def test_p01_arranque_menu_y_cierre(self):
        salida = io.StringIO()
        with patch('builtins.input', side_effect=['1', 'agente', '0', '0']), patch('main.getpass', return_value='AgenteRutaSur1!'), redirect_stdout(salida):
            main(['--db', str(self.ruta)])
        self.assertIn('Crear paquete', salida.getvalue())
        self.assertTrue(Path('README.md').exists())
        self.assertIn('requests', Path('requirements.txt').read_text())

    def test_p02_p03_crear_listar(self):
        p = self.app.crear_paquete(self.agente, PaqueteNacional, 'Puerto Varas 4 días', '450000', 1)
        encontrados = self.app.paquetes.listar()
        self.assertIn(p.id, [x.id for x in encontrados])
        self.assertEqual(self.app.paquetes.buscar(p.id).calcular_precio(), 450000)

    def test_p04_actualizar_precio(self):
        self.app.cambiar_precio(self.agente, 1, '450000')
        self.assertEqual(self.app.paquetes.listar()[0].calcular_precio(), 450000)

    def test_p05_persistencia_otra_conexion(self):
        self.app.cambiar_precio(self.agente, 1, '470000')
        nueva = crear_conexion(self.ruta)
        try:
            self.assertEqual(Agencia(nueva).paquetes.buscar(1).calcular_precio(), 470000)
        finally:
            nueva.close()

    def test_p06_eliminar_paquete_y_subtipo(self):
        self.app.eliminar_paquete(self.agente, 1)
        self.assertIsNone(self.app.paquetes.buscar(1))
        self.assertEqual(self.con.execute('SELECT COUNT(*) FROM paquetes_nacionales').fetchone()[0], 0)

    def test_p07_pasaporte_valido(self):
        r = self.reservar(2, 'F12345678')
        self.assertEqual(self.app.reservas.buscar(r.id).viajeros[0].pasaporte, 'F12345678')

    def test_p08_pasaporte_vacio_y_menu_continua(self):
        with self.assertRaises(PasaporteInvalidoError):
            self.reservar(2)
        salida = self.consola(['17', '1', '2', self.FECHA, '1', 'Ana', '', '1', '0'])
        self.assertIn('pasaporte', salida.lower())
        self.assertIn('Chiloé', salida)
        self.indicador.obtener_dolar.assert_not_called()

    def test_p09_nacional_sin_api(self):
        precio, indicador = self.app.cotizar(self.agente, 1)
        self.assertEqual(precio, 300000)
        self.assertIsNone(indicador)
        self.indicador.obtener_dolar.assert_not_called()

    def test_p10_internacional_convierte(self):
        self.assertEqual(self.app.cotizar(self.agente, 2)[0], 475000)

    def test_p11_crucero_formula_propia(self):
        self.assertEqual(self.app.cotizar(self.agente, 3)[0], 1045000)

    def test_p12_p13_detalles_persisten_y_se_muestran(self):
        r = self.reservar(cantidad=2)
        recuperada = self.app.reservas.buscar(r.id)
        self.assertEqual({d.tipo for d in recuperada.detalles}, set(DetalleReserva.TIPOS))
        self.assertEqual(recuperada.total, 600000)
        salida = self.consola(['5', str(r.id), '0'])
        for tipo in DetalleReserva.TIPOS:
            self.assertIn(f'Servicio {tipo}', salida)

    def test_p14_30_rechaza_50_confirma(self):
        r = self.reservar()
        self.app.registrar_pago(self.admin, r.id, 90000)
        with self.assertRaises(AnticipoInsuficienteError):
            self.app.confirmar(self.agente, r.id)
        salida = self.consola(['18', str(r.id), '1', '0'])
        self.assertIn('50 %', salida)
        self.assertEqual(self.app.reservas.buscar(r.id).estado, 'pendiente')
        self.app.registrar_pago(self.admin, r.id, 60000)
        self.app.confirmar(self.agente, r.id)
        self.assertEqual(self.app.reservas.buscar(r.id).estado, 'confirmada')
        self.assertEqual(self.app.disponibilidad.buscar(1, self.FECHA).cupos_disponibles, 9)

    def test_p15_cero_cupos(self):
        self.app.configurar_cupos(self.admin, 1, self.FECHA, 0)
        with self.assertRaises(SinCuposError):
            self.reservar()
        self.assertEqual(self.app.reservas.listar(), [])

    def test_p16_respuesta_api_persiste_valor_y_fecha(self):
        respuesta = Mock()
        respuesta.json.return_value = {'serie': [{'valor': 950, 'fecha': '2026-10-02T00:00:00Z'}]}
        with patch('servicios.mindicador.requests.get', return_value=respuesta) as get:
            precio, indicador = Agencia(self.con).cotizar(self.agente, 2)
        get.assert_called_once_with('https://mindicador.cl/api/dolar', timeout=5)
        respuesta.raise_for_status.assert_called_once()
        self.assertEqual(precio, 475000)
        self.assertEqual(self.app.cotizaciones.listar()[0]['valor'], '950')
        self.assertEqual(indicador.fecha, '2026-10-02T00:00:00+00:00')

    def test_p17_sin_internet_menu_continua(self):
        self.indicador.obtener_dolar.side_effect = IndicadorNoDisponibleError('Revise la conexión a internet.')
        salida = self.consola(['2', '2', '1', '0'])
        self.assertIn('conexión', salida)
        self.assertIn('Chiloé', salida)
        self.assertEqual(self.app.cotizaciones.listar(), [])

    def test_p18_opcion_99_continua(self):
        salida = self.consola(['99', '1', '0'])
        self.assertIn('Opción inválida', salida)
        self.assertIn('Chiloé', salida)

    def test_p19_abc_precio_y_viajeros_continua(self):
        salida = self.consola(['11', '1', 'abc', '17', '1', '1', self.FECHA, 'abc', '1', '0'])
        self.assertEqual(salida.count('debe ser un número'), 2)
        self.assertIn('Chiloé', salida)

    def test_roles_se_validan_fuera_del_menu(self):
        with self.assertRaises(OperacionNoPermitidaError):
            self.app.crear_cliente(self.admin, 'No permitido', 'a@b.cl')
        with self.assertRaises(OperacionNoPermitidaError):
            self.app.crear_proveedor(self.agente, 'No permitido')
        with self.assertRaises(OperacionNoPermitidaError):
            self.app.registrar_pago(self.agente, 1, 10)
        salida = self.consola(['17', '0'], self.admin)
        self.assertIn('Opción inválida', salida)
        self.assertNotIn('Crear reserva', salida)

    def test_hash_salt_y_password_incorrecto(self):
        fila = self.con.execute('SELECT * FROM usuarios WHERE nombre_usuario = ?', ('agente',)).fetchone()
        self.assertNotEqual(fila['hash_password'], 'AgenteRutaSur1!')
        self.assertEqual(len(fila['salt']), 32)
        self.assertIsNone(Autenticacion(self.con).iniciar_sesion('agente', 'incorrecta'))
        self.assertIsNone(Autenticacion(self.con).iniciar_sesion("' OR 1=1 --", 'incorrecta'))

    def test_sql_parametrizado_y_crud_cliente(self):
        nombre = "O'Reilly'); DROP TABLE clientes; --"
        c = self.app.crear_cliente(self.agente, nombre, 'demo@example.com')
        self.assertEqual(self.app.clientes.buscar(c.id).nombre, nombre)
        self.app.actualizar_cliente(self.agente, c.id, 'Actualizado', 'nuevo@example.com')
        self.assertEqual(self.app.clientes.buscar(c.id).nombre, 'Actualizado')
        self.app.eliminar_cliente(self.agente, c.id)
        self.assertIsNone(self.app.clientes.buscar(c.id))

    def test_crud_proveedor(self):
        p = self.app.crear_proveedor(self.admin, 'Otro operador')
        self.app.actualizar_proveedor(self.admin, p.id, 'Nuevo nombre')
        self.assertEqual(self.app.proveedores.buscar(p.id).nombre, 'Nuevo nombre')
        self.app.eliminar_proveedor(self.admin, p.id)
        self.assertIsNone(self.app.proveedores.buscar(p.id))

    def test_rollback_cabecera_cupos_y_cotizacion(self):
        original = self.app.reservas.insertar
        def fallar(reserva):
            original(reserva)
            raise sqlite3.IntegrityError('Falla simulada después de insertar detalles')
        with patch.object(self.app.reservas, 'insertar', side_effect=fallar):
            with self.assertRaises(sqlite3.IntegrityError):
                self.reservar(2, 'F12345678')
        self.assertEqual(self.app.reservas.listar(), [])
        self.assertEqual(self.app.cotizaciones.listar(), [])
        self.assertEqual(self.app.disponibilidad.buscar(1, self.FECHA).cupos_disponibles, 10)
        self.assertEqual(self.con.execute('SELECT COUNT(*) FROM detalles_reserva').fetchone()[0], 0)

    def test_precio_historico_no_cambia(self):
        r = self.reservar()
        self.app.cambiar_precio(self.agente, 1, '900000')
        self.assertEqual(self.app.reservas.buscar(r.id).total, 300000)

    def test_cancelacion_libera_una_sola_vez(self):
        r = self.reservar(cantidad=2)
        self.app.cancelar(self.agente, r.id)
        with self.assertRaises(OperacionNoPermitidaError):
            self.app.cancelar(self.agente, r.id)
        self.assertEqual(self.app.disponibilidad.buscar(1, self.FECHA).cupos_disponibles, 10)

    def test_sobrepago_y_cancelacion_con_pagos(self):
        r = self.reservar()
        with self.assertRaises(DatosInvalidosError):
            self.app.registrar_pago(self.admin, r.id, r.total + 1)
        self.app.registrar_pago(self.admin, r.id, 1)
        with self.assertRaises(OperacionNoPermitidaError):
            self.app.cancelar(self.agente, r.id)

    def test_no_elimina_paquete_con_reserva(self):
        self.reservar()
        with self.assertRaises(sqlite3.IntegrityError):
            self.app.eliminar_paquete(self.agente, 1)
        self.assertIsNotNone(self.app.paquetes.buscar(1))

    def test_no_reduce_total_bajo_ocupados(self):
        self.reservar(cantidad=2)
        with self.assertRaises(DatosInvalidosError):
            self.app.configurar_cupos(self.admin, 1, self.FECHA, 1)

    def test_no_sobrevende_cupos(self):
        self.app.configurar_cupos(self.admin, 1, self.FECHA, 1)
        self.reservar()
        with self.assertRaises(SinCuposError):
            self.reservar()
        self.assertEqual(len(self.app.reservas.listar()), 1)

    def test_abc_y_reconstruccion_subtipos(self):
        with self.assertRaises(TypeError):
            Paquete('Abstracto', 1, None)
        self.assertIsInstance(self.app.paquetes.buscar(1), PaqueteNacional)
        self.assertIsInstance(self.app.paquetes.buscar(2), PaqueteInternacional)
        self.assertIsInstance(self.app.paquetes.buscar(3), Crucero)

    def test_demo_no_duplica_al_reiniciar(self):
        self.assertFalse(cargar_demo(self.con))
        self.assertEqual(len(self.app.paquetes.listar()), 3)

    def test_precio_negativo_nan_y_vacio(self):
        for precio in ('-1', 'NaN', 'Infinity', '', '0'):
            with self.subTest(precio=precio), self.assertRaises(DatosInvalidosError):
                self.app.cambiar_precio(self.agente, 1, precio)

    def test_total_impar_exige_siguiente_peso(self):
        self.app.cambiar_precio(self.agente, 1, '101')
        r = self.reservar()
        self.app.registrar_pago(self.admin, r.id, 50)
        with self.assertRaises(AnticipoInsuficienteError):
            self.app.confirmar(self.agente, r.id)
        self.app.registrar_pago(self.admin, r.id, 1)
        self.app.confirmar(self.agente, r.id)
        self.assertEqual(self.app.reservas.buscar(r.id).estado, 'confirmada')

    def test_error_api_no_ocupa_cupos_ni_guarda_reserva(self):
        self.indicador.obtener_dolar.side_effect = IndicadorNoDisponibleError('Sin conexión')
        with self.assertRaises(IndicadorNoDisponibleError):
            self.reservar(2, 'F12345678')
        self.assertEqual(self.app.reservas.listar(), [])
        self.assertEqual(self.app.cotizaciones.listar(), [])
        self.assertEqual(self.app.disponibilidad.buscar(1, self.FECHA).cupos_disponibles, 10)


class ApiTest(unittest.TestCase):
    def test_errores_red_http_timeout(self):
        for error in (requests.exceptions.ConnectionError(), requests.exceptions.Timeout(), requests.exceptions.HTTPError()):
            with self.subTest(error=type(error)), patch('servicios.mindicador.requests.get', side_effect=error):
                with self.assertRaises(IndicadorNoDisponibleError):
                    Mindicador().obtener_dolar()

    def test_respuestas_invalidas(self):
        for datos in ({}, {'serie': []}, {'serie': [{'valor': True, 'fecha': '2026-10-02'}]},
                      {'serie': [{'valor': -1, 'fecha': '2026-10-02'}]},
                      {'serie': [{'valor': 950, 'fecha': 'inválida'}]}):
            respuesta = Mock()
            respuesta.json.return_value = datos
            with self.subTest(datos=datos), patch('servicios.mindicador.requests.get', return_value=respuesta):
                with self.assertRaises(IndicadorNoDisponibleError):
                    Mindicador().obtener_dolar()


if __name__ == '__main__':
    unittest.main()
