from model.trabajador import Trabajador


class AgenteViajes(Trabajador):
    @property
    def rol(self):
        return 'agente'

    def puede(self, accion):
        return accion in {'consultar', 'gestionar_paquetes', 'gestionar_clientes', 'reservar'}
