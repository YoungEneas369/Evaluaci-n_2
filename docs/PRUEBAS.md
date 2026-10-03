# Validación del proyecto

Comprobación local inicial: **35 pruebas automáticas aprobadas**, Python 3.13.4, Windows. Comando: `python -m unittest discover -s tests -v`. Las bases de estas pruebas son temporales y las respuestas HTTP se simulan para obtener resultados repetibles. P02/P03 y P12/P13 se agrupan, pero conservan sus comprobaciones.

## Correspondencia con el Excel

| Caso | Cobertura automática | Resultado inicial |
|---|---|---|
| P01 | Arranque, autenticación y menú; archivos README/requirements | Aprobado |
| P02 | Crear Puerto Varas 4 días a 450000 | Aprobado |
| P03 | Listar el paquete creado | Aprobado |
| P04 | Actualizar precio y recuperarlo | Aprobado |
| P05 | Leer el cambio desde otra conexión al archivo | Aprobado |
| P06 | Borrar paquete y fila de subtipo | Aprobado |
| P07 | Aceptar F12345678 en internacional | Aprobado |
| P08 | Rechazar pasaporte vacío y continuar menú | Aprobado |
| P09 | Nacional sin llamada a API | Aprobado |
| P10 | Internacional convertido con dólar simulado 950 | Aprobado |
| P11 | Crucero con cambio y 10 % propio | Aprobado |
| P12 | Guardar los cuatro tipos de detalle | Aprobado |
| P13 | Recuperarlos y mostrarlos por consola | Aprobado |
| P14 | Rechazar 30 %, aceptar 50 %, conservar cupos | Aprobado |
| P15 | Cero cupos impide crear reserva | Aprobado |
| P16 | GET, timeout, extracción y almacenamiento de valor/fecha simulados | Aprobado; consulta real adicional abajo |
| P17 | Fallo de conexión manejado; menú continúa | Aprobado mediante simulación |
| P18 | Opción 99 informa error y continúa | Aprobado |
| P19 | abc en precio o viajeros informa error y continúa | Aprobado |

También se prueban permisos del servicio, autenticación incorrecta, hash y salt, SQL con apóstrofos, CRUD de clientes/proveedores, rollback de reserva/cupos/cotización, precio histórico, cancelación y liberación única, sobrepago, integridad referencial, límites de disponibilidad, abstracción, reconstrucción de subtipos y datos externos inválidos.

## Consulta real

Se ejecutó `Mindicador().obtener_dolar()` contra `https://mindicador.cl/api/dolar` con conexión autorizada. Resultado observado:

```text
USD_CLP= 983.84
FECHA_PUBLICADA= 2026-10-02T03:00:00+00:00
```

Es un dato observado al validar, no una constante del programa ni una promesa de cotización futura. El servicio debe consultarse nuevamente al evaluar. La primera consulta desde el entorno restringido no tuvo conexión; el servicio tradujo correctamente el error y la comprobación con acceso a red obtuvo el valor anterior.

## Alcance de la evidencia

Estos resultados no son una nota ni una firma del profesor. La prueba automatizada del flujo usa entradas simuladas y no sustituye que el estudiante recorra el README en su terminal. La pérdida de red se simula sin apagar la conexión del equipo. No se modificó la planilla original del profesor ni se completaron sus casillas de evaluación.

Antes de entregar, ejecutar en la máquina que se utilizará durante la evaluación y practicar el recorrido del README. Para verificar instalación desde cero, usar un entorno virtual y `python -m pip install -r requirements.txt`; la validación local se realizó con `requests` ya instalado.

El registro íntegro de la última ejecución se conserva en [resultado_pruebas.txt](resultado_pruebas.txt).

El registro íntegro de la última ejecución se conserva en [resultado_pruebas.txt](resultado_pruebas.txt).
