from datetime import datetime, timezone

from dao.dao import DAO


class CotizacionDAO(DAO):
    def insertar(self, indicador):
        return self.ejecutar('''INSERT INTO cotizaciones(codigo, valor, fecha_indicador, consultado_en)
            VALUES (?, ?, ?, ?)''', ('dolar', str(indicador.valor), indicador.fecha,
                                    datetime.now(timezone.utc).isoformat())).lastrowid

    def listar(self):
        return [dict(f) for f in self.ejecutar('SELECT * FROM cotizaciones ORDER BY id').fetchall()]
