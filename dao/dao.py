class DAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def ejecutar(self, sql, parametros=()):
        return self.conexion.execute(sql, parametros)
