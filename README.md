# Agencia de viajes RutaSur

Proyecto académico de Cristopher Figueroa y Elías Reyes. Python, programación orientada a objetos, SQLite y API de dólar observado.

## Ejecutar

Requiere Python 3.10 o superior e internet para instalar `requests` y cotizar paquetes internacionales o cruceros.

Desde esta carpeta:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Se crea automáticamente `data/rutasur.db`. Los cambios persisten entre ejecuciones. Los datos ficticios se cargan únicamente cuando no hay usuarios.

| Usuario de demostración | Contraseña | Responsabilidad |
|---|---|---|
| agente | AgenteRutaSur1! | Clientes, paquetes y reservas |
| admin | AdminRutaSur1! | Proveedores, disponibilidad y pagos |

Estas credenciales públicas son exclusivamente de demostración académica. En la base se almacena un hash PBKDF2 con salt aleatoria, no la contraseña. La contraseña no se muestra mientras se escribe en una terminal compatible.

## Recorrido para la evaluación

1. Iniciar sesión como `agente`. Opción **1** muestra los tres paquetes iniciales; **3** muestra proveedor y fecha con cupos (30 días después del primer inicio).
2. **10** crea un paquete: tipo `1`, nombre `Puerto Varas 4 días`, precio `450000`, proveedor `1`. **1** lista, **11** modifica el precio y **12** elimina un paquete sin reservas. Salir y ejecutar otra vez verifica persistencia.
3. **2** cotiza: nacional no usa internet; internacional y crucero consultan `https://mindicador.cl/api/dolar`. Se muestra el valor y la fecha publicada. El crucero añade 10 % de servicio.
4. **17** crea una reserva: cliente `1`, paquete elegido, fecha con cupos, cantidad de viajeros y sus nombres. Internacional pide pasaporte, por ejemplo `F12345678`. Ingresar las cuatro descripciones para vuelo, hotel, seguro y excursión. **4** lista reservas y **5** recupera sus detalles.
5. Cerrar sesión con **0**, entrar como `admin`, **24** registrar un pago del 30 % del total. Volver a `agente`, **18** intentar confirmar: debe rechazar y mantener el programa abierto.
6. Con `admin`, **24** completar otro 20 %. Con `agente`, **18** confirmar: debe aceptar. El total y el saldo aparecen en **5**.
7. Con `admin`, **23** configurar proveedor `1`, una fecha nueva y cupos `0`. Con `agente`, intentar reservar esa fecha: debe rechazar por falta de cupos.
8. Introducir `99` como opción o `abc` en precio/cantidad: se informa el problema y continúa el menú.

Ingresar números sin separador de miles; los decimales USD usan punto. Los pagos se expresan en pesos enteros. Todos los precios son **por viajero e incluyen los ítems**. El cliente comprador puede ser distinto de los viajeros.

## Organización y decisiones

- `model/`: objetos, herencia, clases abstractas, validaciones y reglas de negocio.
- `dao/`: SQL parametrizado y reconstrucción de objetos.
- `servicios/`: autenticación, API, cotización y coordinación de transacciones/permisos.
- `main.py`: entradas y salidas de consola; captura errores recuperables.
- `conectar.py`: único punto que abre conexiones SQLite.
- [Decisiones y trazabilidad](docs/DECISIONES.md): exigencias y supuestos separados.
- [Diagrama de clases](docs/DIAGRAMA.md): modelo implementado y relaciones.
- [Pruebas](docs/PRUEBAS.md): cobertura del guion y resultados verificables.
- [Guía de defensa](docs/DEFENSA.md): recorrido del código y preguntas de práctica.
- [Instrucciones de las clases](docs/INSTRUCCIONES_CLASES.md): recopilación de referencia.

## Pruebas automáticas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas usan bases temporales y respuestas de API simuladas. No modifican la base normal. Para otra base de demostración: `python main.py --db prueba.db`.

Las transacciones usan `with conexion`: confirma al terminar y revierte ante una excepción. La conexión permanece abierta durante la sesión y se cierra en `finally`. Una reserva guarda cabecera, viajeros, detalles, cotización y descuento de cupos como una sola operación. Los pagos y cambios de estado bloquean escritura antes de leer para evitar decisiones basadas en saldos obsoletos.

La versión cubre el guion académico: cancelación únicamente sin pagos y disponibilidad compartida por proveedor/fecha. No integra pagos bancarios ni verificaciones oficiales de identidad.
