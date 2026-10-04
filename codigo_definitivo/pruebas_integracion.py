"""Comprobar con: python -B -m unittest pruebas_integracion -v"""
import unittest

from cliente import Cliente
from persona import Persona
from viajero import Viajero
from trabajador import Trabajador
from agente_viajes import AgenteViajes
from administrador import Administrador
from paquete_nacional import PaqueteNacional
from paquete_internacional import PaqueteInternacional
from crucero import Crucero


class IntegracionEquipo(unittest.TestCase):
    def test_comprador_conserva_contacto_sin_pasaporte(self):
        comprador = Cliente("Ana", "RUT-DEMO", "ana@example.com", "123")
        self.assertIsInstance(comprador, Persona)
        self.assertEqual(comprador.correo, "ana@example.com")
        self.assertEqual(comprador.telefono, "123")
        self.assertFalse(hasattr(comprador, "pasaporte"))

    def test_cambio_invalido_conserva_nombre_y_contacto(self):
        comprador = Cliente("Ana", "RUT-DEMO", "ana@example.com", "123")
        with self.assertRaises(ValueError):
            comprador.cambiar_nombre(" ")
        self.assertEqual(comprador.nombre, "Ana")
        comprador.cambiar_nombre(" Ana Pérez ")
        self.assertEqual(comprador.nombre, "Ana Pérez")
        self.assertEqual(comprador.correo, "ana@example.com")

    def test_constructor_aplica_validacion_del_padre(self):
        with self.assertRaises(ValueError):
            Cliente(" ", "RUT-DEMO", "ana@example.com", "123")
        with self.assertRaises(ValueError):
            Cliente("Ana", " ", "ana@example.com", "123")

    def test_pasaporte_aceptado_y_ausencia_rechazada_al_validar(self):
        viajero = Viajero("Elena", "F12345678")
        viajero.validar_pasaporte()
        self.assertEqual(viajero.pasaporte, "F12345678")
        for ausencia in (None, "", "   "):
            with self.subTest(ausencia=ausencia):
                viajero.pasaporte = ausencia
                with self.assertRaises(ValueError):
                    viajero.validar_pasaporte()

    def test_roles_comparten_trabajador(self):
        # Dato de prueba, no una contraseña ni autenticación implementada.
        agente = AgenteViajes("Ana", "RUT-DEMO", "ana", "hash_de_prueba")
        admin = Administrador("Luis", "RUT-DEMO", "luis", "hash_de_prueba")
        self.assertIsInstance(agente, Trabajador)
        self.assertIsInstance(admin, Persona)
        self.assertTrue(agente.puede_atender_clientes())
        self.assertFalse(admin.puede_atender_clientes())

    def test_totales_de_los_tres_paquetes(self):
        nacional = PaqueteNacional("Sur", 150000)
        self.assertEqual(nacional.calcular_total(2), 300000)
        self.assertEqual(nacional.calcular_total(2, 950), 300000)
        self.assertEqual(PaqueteInternacional("Tokio", 500).calcular_total(2, 950), 950000)
        self.assertAlmostEqual(Crucero("Caribe", 800, 7).calcular_total(2, 950), 1672000)

    def test_paquetes_en_usd_necesitan_cambio(self):
        for paquete in (PaqueteInternacional("Tokio", 500), Crucero("Caribe", 800, 7)):
            for cambio in (None, 0, -1):
                with self.subTest(tipo=type(paquete).__name__, cambio=cambio):
                    with self.assertRaises(ValueError):
                        paquete.calcular_total(2, cambio)

    def test_noches_son_solo_lectura(self):
        crucero = Crucero("Caribe", 800, 7)
        self.assertEqual(crucero.noches, 7)
        with self.assertRaises(AttributeError):
            crucero.noches = 10


if __name__ == "__main__":
    unittest.main()
