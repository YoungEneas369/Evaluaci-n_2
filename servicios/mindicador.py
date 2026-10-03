import requests

from excepciones import DatosInvalidosError, IndicadorNoDisponibleError
from model.tipo_cambio import TipoCambio


class Mindicador:
    URL = 'https://mindicador.cl/api/dolar'

    def __init__(self, timeout=5):
        self.__timeout = timeout

    def obtener_dolar(self):
        try:
            respuesta = requests.get(self.URL, timeout=self.__timeout)
            respuesta.raise_for_status()
            datos = respuesta.json()
            fila = datos['serie'][0]
            if isinstance(fila['valor'], bool):
                raise ValueError('Valor booleano')
            return TipoCambio(fila['valor'], fila['fecha'])
        except requests.exceptions.Timeout:
            raise IndicadorNoDisponibleError('La consulta del dólar tardó demasiado. Intente nuevamente.') from None
        except requests.exceptions.ConnectionError:
            raise IndicadorNoDisponibleError('No se pudo obtener el dólar: revise la conexión a internet.') from None
        except requests.exceptions.HTTPError:
            raise IndicadorNoDisponibleError('El servicio del dólar respondió con un error HTTP.') from None
        except (ValueError, KeyError, IndexError, TypeError, DatosInvalidosError):
            raise IndicadorNoDisponibleError('El servicio no entregó un valor y una fecha válidos.') from None
        except requests.exceptions.RequestException:
            raise IndicadorNoDisponibleError('No se pudo completar la consulta del dólar.') from None
