# Preparación para explicar el código

Primero ejecuta el recorrido del README. Después estudia este camino: `main.py` → `servicios/agencia.py` → `model/reserva.py` → `dao/reserva_dao.py`. Sigue una reserva concreta, por ejemplo un nacional de $300.000 para dos viajeros, total $600.000 y anticipo mínimo $300.000.

## Preguntas y claves para comprobar tu explicación

1. **¿Qué es una clase y qué es un objeto en este proyecto?** `PaqueteNacional` describe estructura y comportamiento; el objeto «Chiloé 3 días» es una instancia con nombre, precio, proveedor e identificador propios. `self` identifica la instancia que ejecuta el método.
2. **¿Por qué Paquete es abstracta?** Define un contrato de cálculo compartido. `ABC` y `abstractmethod` impiden crear un paquete genérico que no implemente los métodos abstractos. Revisa `model/paquete.py` y sus tres hijas.
3. **¿Dónde está el polimorfismo?** En `servicios/cotizador.py`: la misma llamada `calcular_precio` ejecuta la implementación del tipo concreto. Con dólar 950 y base 1.000 USD, internacional da 950.000 y crucero 1.045.000. Nacional usa su base CLP sin consultar API.
4. **¿Qué hereda un administrador?** Hereda nombre y contrato de permisos desde `Persona` y `Trabajador`. No hereda atención de clientes. `puede` y `exigir_permiso` restringen operaciones incluso si se invoca directamente el servicio.
5. **¿Para qué sirven los atributos privados y las propiedades?** Evitan modificar el estado por cualquier camino sin validarlo. El setter de `precio_base` rechaza un valor negativo. En Python el prefijo doble aplica transformación de nombre; no es una barrera de seguridad absoluta.
6. **¿Por qué Cliente y Viajero son diferentes?** Alguien puede comprar para otra persona. El pasaporte pertenece al viajero que realizará el viaje. Se valida al registrar y nuevamente antes de confirmar internacionales.
7. **¿Por qué los detalles no aumentan el total?** Se eligió precio de paquete con servicios incluidos. El detalle documenta vuelo, hotel, seguro o excursión. Volver a sumarlos produciría doble cobro. El total multiplica el precio unitario por viajeros.
8. **¿Qué sucede si se intenta confirmar con 30 %?** `Reserva.confirmar` lanza `AnticipoInsuficienteError`. La transacción se revierte, el estado sigue pendiente y el menú captura el error. Al llegar a 50 % permite confirmar.
9. **¿Cuándo se ocupan los cupos?** Al crear la reserva pendiente. `UPDATE ... WHERE cupos_disponibles >= ?` descuenta solo si alcanza. Si algo falla después, se revierte también ese descuento. Confirmar no vuelve a descontar.
10. **¿Qué hacen commit, rollback y finally aquí?** El bloque `with conexion` confirma o revierte todas sus escrituras conjuntamente. `finally` cierra la conexión al terminar la sesión. Cerrar una conexión no sustituye confirmar cambios.
11. **¿Por qué usamos signos ? en SQL?** Los valores se envían separados de las instrucciones SQL. Un nombre con apóstrofo se guarda como dato. No concatenamos entradas del usuario en la consulta.
12. **¿Qué devuelve un DAO?** `buscar` reconstruye un objeto con sus relaciones o devuelve `None`; `listar` devuelve objetos. El historial de cotizaciones es una consulta de datos y devuelve diccionarios. El DAO no muestra mensajes de consola.
13. **¿Qué ocurre cuando falla internet?** `Mindicador` traduce fallos de red/HTTP/datos a `IndicadorNoDisponibleError`; el menú informa y continúa. El modelo no sabe de HTTP. No se inventa un dólar de respaldo.
14. **¿Por qué guardamos precio y cotización de la reserva?** Una reserva acordada no cambia de precio al modificar después un paquete o al subir el dólar. Guardamos el precio CLP por viajero y la referencia al dato utilizado.
15. **¿Cómo se guardan las contraseñas?** PBKDF2 aplica SHA-256 repetidamente con una salt aleatoria. Se compara el hash calculado, no el texto de la contraseña. La base de demostración no contiene contraseñas en texto plano; sus claves de acceso están publicadas en README porque son datos académicos.

## Ejercicios de razonamiento

- Si una reserva cuesta $101, ¿bastan $50 de anticipo? No: `50 * 2 < 101`. Se requieren $51.
- Si hay dos cupos y llegan tres viajeros, ¿qué tablas quedan modificadas? Ninguna: la operación se rechaza; cualquier escritura dentro de la transacción se revierte.
- Si se elimina el control de permisos del menú, ¿queda protegido el servicio? Las mutaciones aún llaman a `exigir_permiso`. El menú es presentación; el servicio aplica autorización.
- Si una reserva pendiente ya ocupó un cupo y se confirma dos veces, ¿se descuentan más cupos? No. Confirmar exige estado pendiente y no descuenta cupos.
- Si el comprador no viaja, ¿a quién se pide pasaporte? A cada viajero internacional, no al comprador.

## Simulación acordada

La práctica oral se hace una pregunta a la vez, con tu respuesta primero. Después se revisa exactitud, explicación con tus palabras y ubicación en el código. Esta guía prepara la práctica; leerla no equivale a haber realizado la defensa. La primera pregunta será: «¿Dónde está el polimorfismo en RutaSur y qué ocurre cuando cotizas un nacional y un crucero?».
