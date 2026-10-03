from model.trabajador import Trabajador


class Administrador(Trabajador):
    @property
    def rol(self):
        return 'administrador'

    def puede(self, accion):
        return accion in {'consultar', 'gestionar_proveedores', 'registrar_pagos'}
