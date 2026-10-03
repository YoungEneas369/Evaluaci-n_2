# Decisiones y trazabilidad de RutaSur

Autores: Cristopher Figueroa y Elías Reyes. Implementación preparada a partir del enunciado recibido, las clases y el guion específico de Agencia de Viajes. Las decisiones siguientes completan vacíos del enunciado; no se atribuyen al profesor.

## Problema y solución

La agencia vende viajes nacionales, internacionales y cruceros. Necesita mantener sus paquetes, registrar quién compra y quién viaja, guardar los servicios incluidos y comprobar pagos y cupos antes de comprometer una reserva. El cálculo varía según el tipo de paquete. Un único precio genérico, un pasaporte en el comprador o cupos sin fecha no representan correctamente estas necesidades.

Se usa una aplicación de consola con objetos de dominio, servicios y DAO. SQLite conserva los datos y Mindicador proporciona el dólar observado. El agente se encarga de clientes y reservas; el administrador administra proveedores, disponibilidad y pagos. Ambos pueden consultar información, pero los permisos de escritura se verifican también en el servicio.

## Reglas confirmadas y su implementación

| Fuente | Regla | Código principal |
|---|---|---|
| Enunciado | Tres tipos con cálculo diferente | `Paquete` abstracto; `PaqueteNacional`, `PaqueteInternacional`, `Crucero` |
| Enunciado | Nacional no requiere cambio; otros sí | `Cotizador.cotizar`, propiedades de `Paquete` |
| Enunciado | Agente y administrador tienen responsabilidades distintas | `Trabajador`, sus dos hijas y `Usuario.exigir_permiso` |
| Enunciado / P07–P08 | Validar pasaporte de viajero internacional | `Viajero.validar_pasaporte`, creación y confirmación |
| Enunciado / P12–P13 | Reserva con varios detalles recuperables | `Reserva`, `DetalleReserva`, `ReservaDAO` |
| P14 | Anticipo mínimo 50 % | `Reserva.confirmar`: `pagado * 2 < total` |
| P15 | No reservar sin cupos por proveedor/fecha | `Disponibilidad`, `DisponibilidadDAO.ocupar` |
| P16–P17 | API dólar y manejo de desconexión | `Mindicador`, `Cotizador`, excepciones y menú |
| P01–P06 | CRUD persistente | `PaqueteDAO`, transacciones, SQLite y README |
| P18–P19 | Entrada inválida no cierra aplicación | `validaciones.py`, `Consola.ejecutar` |
| Clases S7–S10 | Herencia, ABC, excepciones, DAO y SQL seguro | Modelo, tablas padre/hija, DAO parametrizados |
| Antecedentes generales de evaluación | Autenticación y almacenamiento del indicador | `Autenticacion`, `UsuarioDAO`, `CotizacionDAO` |

La autenticación y el historial amplían la cobertura técnica de las referencias generales; no aparecen como casos independientes en las 19 filas del Excel específico.

## Supuestos elegidos para esta versión

1. **Precio por viajero con servicios incluidos.** Los detalles explican lo contratado y no añaden cobros. Total = precio final individual × viajeros.
2. **Fórmulas simples.** Nacional: base CLP. Internacional: base USD × dólar. Crucero: base USD × dólar × 1,10 (servicio del 10 %). Ese porcentaje es decisión de implementación, no exigencia del profesor. Se redondea el precio individual a pesos enteros con `ROUND_HALF_UP`; `Decimal` evita los errores habituales de representación binaria de dinero.
3. **Uno o más viajeros.** El comprador es `Cliente`, el viajero es `Viajero`; no tienen que ser la misma persona. La lista de viajeros se guarda dentro de cada reserva, como fotografía de los datos proporcionados para ese viaje.
4. **Pasaporte académico.** Entre 6 y 12 caracteres alfanuméricos; se normalizan letras a mayúsculas. Acepta `F12345678`, rechaza vacío. No certifica identidad ni vencimiento. Se exige a internacionales; extenderlo a cruceros internacionales requeriría modelar el itinerario.
5. **Un proveedor organizador por paquete.** Administra un fondo común de cupos por fecha, compartido por sus paquetes. No se modela un inventario independiente por vuelo/hotel.
6. **Se ocupan cupos al crear la reserva pendiente.** Así dos reservas pendientes no consumen el mismo lugar. Confirmar no vuelve a descontar. Cancelar sin pagos libera cupos una vez. No hay vencimiento automático ni devolución de pagos en esta versión.
7. **Fecha explícita y válida.** Se permiten fechas de calendario sin imponer que sean futuras: el guion no fija esa restricción y facilita repetir pruebas. Una fecha sin disponibilidad registrada no se puede reservar.
8. **Pagos parciales acumulables.** El administrador registra abonos positivos en pesos enteros; no puede superar el saldo. Exactamente 50 % permite confirmar; en totales impares se requiere el siguiente peso entero.
9. **Precio acordado conservado.** Al reservar se guarda el precio CLP por viajero y la referencia al indicador utilizado. Cambios posteriores del catálogo o del dólar no recalculan reservas existentes.
10. **Dólar publicado.** Se usa el primer registro de `serie`, mostrando su fecha. En días sin publicación no se inventa un valor ni se presenta como cotización de ese día. Si la API falla, la operación dependiente del dólar se cancela con mensaje; los nacionales siguen disponibles.
11. **Catálogo de tipos sencillo.** Los cuatro tipos de detalle son constantes validadas en `DetalleReserva.TIPOS` y mediante `CHECK` en SQLite. Conserva el concepto de catálogo del feedback, sin una clase/tabla editable `TipoItem`, porque no hay CRUD de tipos en el guion. No se crean cuatro subclases sin comportamiento distinto.
12. **Eliminación con integridad.** Se pueden borrar paquetes sin reservas. SQLite impide borrar padres referenciados; no se destruye un historial de ventas por borrar un paquete, cliente o proveedor.

## Por qué existen las clases

`Persona` reúne el nombre común de clientes, viajeros y trabajadores. `Trabajador` define el contrato de rol y permisos, sin imponer atención al cliente a un administrador. `Usuario` representa el acceso al sistema y contiene el trabajador que actúa. La identidad de acceso no se mezcla con el comprador.

`Paquete` reúne nombre, precio y proveedor y obliga a definir el cálculo. Sus hijas implementan la variación real del negocio. `Proveedor` representa al organizador; `Disponibilidad` expresa cuántos cupos tiene para una fecha. `Reserva` conserva comprador, paquete, viajeros, detalles, pagos y estado. `DetalleReserva` expresa cada servicio incluido; `Pago` conserva un abono. `TipoCambio` valida el valor y la fecha de una respuesta externa.

Los DAO transforman objetos en filas y filas en objetos. `Agencia` coordina las reglas que requieren varios objetos y una transacción. `Mindicador` conoce HTTP; `Cotizador` conecta la consulta con el cálculo polimórfico. El modelo no importa `requests` ni consulta SQLite.

## Adaptaciones respecto del taller

Se mantiene la separación `model/dao/servicios`, las propiedades, la herencia y las tablas padre/hija. Se completan operaciones que faltaban en el ejemplo y se centraliza el cierre de la conexión. Los DAO no ejecutan `commit` por separado. La coordinación transaccional está en `Agencia`, invocada por `main`, para que también funcione correctamente al probar el servicio sin consola.

En Python, `with conexion` llama a commit al salir correctamente y rollback al salir con una excepción; no cierra la conexión. `main` la cierra en `finally`. `BEGIN IMMEDIATE` es control de transacción para pagos, cambios de estado y cupos; el SQL de entidades permanece en DAO.

La herencia se representa con generalización en el diagrama, no con diamantes. El pasaporte pertenece exclusivamente al viajero. No se crean atributos estáticos para los datos particulares de cada objeto. Las relaciones y el diagrama describen este código; no se presenta el modelo de referencia del profesor como si fuera la entrega original del estudiante.

## Fuentes

- Enunciado transcrito por el estudiante en la conversación.
- `12 - Agencia de viajes - Guion de pruebas.xlsx`, hojas «Guion de pruebas» e «Instrucciones», 19 casos de las filas 11–29.
- [Taller Mecánico del profesor](https://github.com/michaelarjelm/taller-mecanico-114-2A-f2), revisión local `8ec1492083fb1b3f0268332adce97f73e96324a9`.
- [Correcciones del equipo](https://github.com/michaelarjelm/inacapclases/tree/main/2026/semestre2/bimestre1/poos/114-2B-F1/114-2A-F2/ES1-correcciones/12-Agencia-Viajes-Cristopher-Figueroa-Elias-Reyes), revisión local `570f59d31565e458ee2b247171973827a56f656b`.
- [Recopilación de las seis clases](INSTRUCCIONES_CLASES.md), con sus enlaces originales y distinción entre prompts y explicaciones.

Una pauta adicional del profesor podría precisar convenciones o presentación. Estos documentos no sustituyen una rúbrica que no se haya recibido.
