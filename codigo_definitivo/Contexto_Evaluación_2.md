# Contexto de Evaluación 2 — RutaSur

Actualizado: 4 de octubre de 2026. Equipo: Cristopher Figueroa y Elías Reyes.

## 1. Objetivo y alcance de esta carpeta

Estamos reconstruyendo desde cero el programa de una agencia de viajes llamada RutaSur para comprenderlo y poder defenderlo ante el profesor. La prioridad actual es aprender, no generar de una vez el sistema completo.

El estudiante pidió explícitamente seguir el mismo orden de los ejercicios del profesor, adaptados a nuestro negocio. Ante un «siguiente», avanzar un ejercicio pequeño, explicar el cambio y ejecutarlo. Ante una pregunta, detener el avance y aclarar el concepto.

Repositorio del equipo: https://github.com/YoungEneas369/Evaluaci-n_2

Carpeta de aprendizaje compartida: `codigo_definitivo/`. Aunque se llama «definitivo», su contenido todavía está en construcción y no cumple toda la evaluación.

El resto del repositorio contiene una implementación anterior y documentación más avanzada. Puede servir como referencia; no copiarla entera ni confundirla con el punto actual del aprendizaje. Para saber qué se está estudiando, leer los archivos de esta carpeta.

## 2. Punto exacto en que vamos

Completamos S6-P08: reemplazamos los getters por propiedades de lectura (@property) y ajustamos main.py para consultarlas sin paréntesis. Sigue S6-P09: comparar dos objetos y comprobar que cambiar uno no modifica el otro.

Archivos actuales:

| Archivo | Contenido |
| --- | --- |
| `cliente.py` | `Cliente`, con nombre, correo y teléfono privados; constructor; `cambiar_nombre`, `cambiar_correo`, `cambiar_telefono`; propiedades de lectura `nombre`, `correo`, `telefono` |
| `paquetesAgencia.py` | Solo `PaqueteNacional`, con nombre y precio por viajero privados, propiedades de lectura y `calcular_total(cantidad_viajeros)` |
| `main.py` | Crea dos clientes, consulta y cambia datos; crea un paquete nacional de 150000 CLP por viajero y calcula 300000 CLP para dos viajeros |
| `README.md` | Estado resumido e instrucciones para ejecutar |
| Este archivo | Contexto para continuar con otra IA o con el compañero |

Ejecutar desde esta carpeta con Python 3:

```console
python main.py
```

No hay librerías externas necesarias en esta etapa. La ejecución del ejemplo se comprobó correctamente. Eso no equivale a aprobar el guion completo de evaluación.

Todavía no hay en esta versión: herencia, clase abstracta Paquete, internacional, crucero, reservas, viajeros, base de datos, autenticación, API ni menú interactivo. Los datos de los ejemplos se escriben en el código y se mantienen en memoria.

## 3. Cómo explicar al estudiante

El estudiante está aprendiendo los fundamentos. Evitar dar por entendidos «objeto», «inicializar», «parámetro», «atributo», «self» o «retorno». Explicar con un ejemplo concreto y seguir el recorrido del dato.

Le confundía que el parámetro y el atributo se llamaran igual. Le resultó más claro:

```python
def __init__(self, nombre_recibido: str):
    self.__nombre = nombre_recibido
```

Conservar nombres como `nombre_recibido`, `correo_recibido`, `telefono_recibido` y `correo_nuevo` mientras ayuden a comprender. En ese ejemplo reducido, el parámetro recibe el dato y el atributo lo conserva dentro del objeto. El constructor real de Cliente recibe los tres datos.

Ideas ya explicadas que conviene reforzar:

- Una clase describe sus objetos; un objeto representa un cliente particular con sus datos.
- `__init__` inicializa el objeto con valores iniciales cuando se llama a la clase.
- `self` es la referencia al objeto sobre el que está actuando el método; Python la pasa automáticamente en estas llamadas.
- En `a = b`, se evalúa la derecha y se asigna al destino de la izquierda. `a` no es por eso una función.
- `self.__nombre` es un atributo; `nombre_recibido` es un parámetro. No se distinguen solo por estar a izquierda o derecha.
- `return` entrega un resultado a quien llama; `=` asigna; `print` muestra en consola. Son operaciones diferentes.
- Un método con `-> None` no entrega un resultado útil; eso no significa por sí solo que modifique un objeto. Nuestros métodos `cambiar_...` sí lo modifican.
- Las anotaciones `str`, `int` y `float` no validan ni convierten automáticamente los valores.
- El prefijo `__` cambia internamente el nombre del atributo para evitar accesos accidentales; no constituye seguridad absoluta.
- `get` no es una palabra especial de Python: es una convención para nombrar métodos que consultan datos. Podría llamarse obtener_nombre. def define el método y return entrega el resultado.
- Renombramos get_nombre a nombre por elección propia: @property no elimina get_ automáticamente. El decorador permite consultar cliente.nombre sin paréntesis y ejecuta el método de lectura.
- Las propiedades actuales son de solo lectura: cliente.nombre = otro_valor produce AttributeError. Para cambiarlo usamos cambiar_nombre. Se verificaron lectura, cambio por método y rechazo de asignación directa.

El estudiante escribe sus propios comentarios y ejemplos. Leer los archivos antes de editar y conservar sus aportes, corrigiendo con explicación las imprecisiones. No avanzar varios ejercicios en una sola respuesta ni introducir arquitectura avanzada antes de la clase correspondiente.

## 4. Secuencia de clases y adaptación

La secuencia procede del resumen local de seis clases compartidas: S6, S7, S8, S9, S10 y S15. No asumir que tenemos todas las sesiones intermedias ni una pauta técnica completa de la sección.

| Paso S6 | Ejercicio del profesor | Adaptación y estado |
| --- | --- | --- |
| P01 | Vehiculo vacío y comentado | Cliente vacío: completado |
| P02 | Atributos con tipos, sin constructor | Nombre, correo y teléfono: completado |
| P03 | Constructor y estado inicial | Constructor de Cliente: completado |
| P04 | main, crear objeto y mostrar datos | Ejemplos de clientes: completado |
| P05 | Métodos ingresar/entregar, sin retorno útil | Cambiar datos de contacto; el estudiante añadió cambiar_nombre: completado |
| P06 | LineaDetalle, cantidad × precio y subtotal con retorno | PaqueteNacional: viajeros × precio por viajero: completado |
| P07 | Atributos privados y getters públicos | Aplicado a Cliente y PaqueteNacional: completado |
| P08 | Reemplazar getters por properties | Completado en ambas clases |
| P09 | Dos objetos; modificar solo uno y comparar | Pendiente como ejercicio explícito, aunque ya usamos dos clientes |

La adaptación de P06 fue intencional: en RutaSur los detalles están incluidos en el precio del paquete, por lo que no debemos introducir un doble cobro sumando nuevamente sus servicios.

Después de S6:

- S7: herencia, clases hijas, `super`, sobrescritura, encapsulamiento y validaciones. Incorporar los tipos de paquete con el mismo contrato de cálculo y avanzar en pasos pequeños.
- S8: clases abstractas, excepciones y reglas que bloquean operaciones.
- S9: SQLite, conexión, tablas, relaciones y organización con modelo/DAO.
- S10: CRUD parametrizado, persistencia y transacciones (`commit`, `rollback`, cierre).
- S15: consumo de API, deserialización, separación de consulta y cálculo, timeout y manejo de fallos.

Antes de implementar cada sesión posterior, consultar el material del profesor disponible. Este contexto resume la secuencia; no reemplaza todos sus ejercicios. Al terminar el proyecto se acordó simular una defensa: una pregunta sobre código real por vez, respuesta del estudiante primero y retroalimentación después.

## 5. Internacional, crucero y dólar

El estudiante creó por iniciativa propia PaqueteInternacional y PaqueteCrucero, ambas con el mismo cálculo del nacional. La práctica funcionaba, pero no implementaba las diferencias del negocio. Pidió eliminarlas para continuar en orden y se retiraron junto con sus ejemplos e importaciones.

No están descartadas del proyecto. Se retomarán al estudiar herencia y polimorfismo. Se explicó que podemos practicar primero con una cotización explícitamente ficticia y conectar después la API. Por ejemplo: 500 USD por viajero × 950 CLP/USD × 2 viajeros = 950000 CLP. Ese 950 es solo didáctico, no una cotización real ni un reemplazo silencioso ante una falla de red.

La API proporciona el indicador; el modelo calcula el precio. El servicio indicado por el guion es `https://mindicador.cl/api/dolar`. Al implementarlo, comprobar la respuesta real y su fecha: el último valor publicado puede ser de un día anterior. No presentarlo falsamente como publicado hoy.

## 6. Requisitos del negocio

Del enunciado y del feedback del equipo:

- Hay paquetes nacionales, internacionales y cruceros con cálculos distintos. Nacional se calcula en pesos sin depender del dólar; internacional y crucero usan tipo de cambio.
- AgenteViajes arma y vende paquetes y atiende clientes. Administrador gestiona proveedores y pagos y no atiende directamente al cliente. Ambos deben heredar de Trabajador; no poner atención al cliente en el padre común.
- Cliente es el comprador y Viajero es quien viaja. El pasaporte pertenece al viajero, no al comprador; se valida antes de confirmar una reserva internacional.
- Reserva contiene varios DetalleReserva, por ejemplo vuelo, hotel, seguro y excursión. Es composición. TipoItem es un catálogo compartido que debe conservarse.
- Proveedor y Disponibilidad representan cupos por fecha.
- Las especializaciones de Paquete y Trabajador se modelan con herencia, no composición.

El diseño de referencia propuesto contempla Trabajador, AgenteViajes, Administrador, Cliente, Viajero, Paquete, PaqueteNacional, PaqueteInternacional, Crucero, Reserva, DetalleReserva, TipoItem, Pago, Proveedor, Disponibilidad y TipoCambio. Es una propuesta de diseño, no una lista de clases ya implementadas ni una obligación de generarlas ahora.

## 7. Guion de pruebas recibido: P01–P19

El guion específico del equipo fue leído desde una copia local del Excel. La sección indicada es 114-2A-F2. Esta lista resume requisitos; no registra resultados de pruebas contra el proyecto actual.

| Pruebas | Comportamiento esperado en la entrega futura |
| --- | --- |
| P01 | Descargar, instalar dependencias indicadas y ejecutar con menú según README |
| P02–P06 | Crear, listar, modificar precio, conservar al reiniciar y eliminar; paquete nacional de ejemplo «Puerto Varas 4 días», 450000 CLP |
| P07–P08 | Aceptar pasaporte F12345678; rechazar vacío, avisar y continuar |
| P09 | Nacional en CLP sin conversión |
| P10 | Internacional convertido de USD a CLP con dólar consultado |
| P11 | Crucero con tipo de cambio y fórmula propia |
| P12–P13 | Una reserva con varias líneas de servicios; recuperar todas sus líneas |
| P14 | Impedir confirmar con menos del 50 % de anticipo; el ejemplo usa 30 % |
| P15 | Impedir reservar cuando el proveedor no tiene cupos para la fecha |
| P16 | Consultar y comparar el dólar con la API indicada |
| P17 | Fallo sin internet: informar y continuar sin fingir una consulta exitosa |
| P18 | Opción de menú inválida, como 99: avisar y continuar |
| P19 | Texto como abc en un monto o cantidad: avisar y continuar |

Reservar y confirmar no son lo mismo: falta de cupos bloquea reservar; anticipo insuficiente bloquea confirmar.

La referencia técnica general de ES2 también contempla POO, manejo de excepciones, conexión a BD, CRUD parametrizado, autenticación con hash y datos de API deserializados y persistidos. Esa página corresponde a 114-2B-F1, distinta de la sección del guion del equipo. Conservarla como referencia y confirmar alcance técnico cuando corresponda; no trasladar sus fechas o porcentajes de nota ni afirmar que es la pauta completa de nuestra sección.

## 8. Decisiones y límites

- Acordado para la implementación: precio por viajero con servicios incluidos. No sumar otra vez los detalles al total.
- Anticipo: 50 % según el guion. La antigua propuesta de 20 % quedó descartada.
- El recargo de crucero del 10 % no está fijado por el profesor. Definir y justificar una fórmula cuando llegue ese paso.
- No inventar una regla oficial de pasaporte a partir del ejemplo. El guion exige aceptar F12345678 y rechazar vacío; longitud/formato adicional sigue pendiente.
- El ejemplo calcula varias plazas, pero aún no implementa una reserva ni resuelve toda la gestión de varios viajeros.
- Redondeo, pagos acumulados, conservación del precio/cotización, retención/liberación de cupos y cancelaciones requieren decisiones explícitas al implementarse. Existen propuestas en documentos más avanzados; no confundirlas con código de esta carpeta.
- No completar el guion con «Cumple» solo por leer requisitos o ejecutar este ejemplo pequeño.

## 9. Trabajo compartido y publicación

El usuario pidió publicar esta carpeta para que su compañero siga el mismo avance. Mantener el contexto actualizado cuando cambie la etapa. Antes de editar o subir, revisar estado y diferencias para conservar trabajo ajeno y evitar incluir otros cambios del repositorio.

En el equipo de origen, el código de estudio se edita en `C:\Evaluación_2\codigo_definitivo` y hay una copia publicada en `C:\Evaluación_2\agencia_viajes\codigo_definitivo`. Son dos carpetas, no una sincronización automática. Al publicar hay que verificar que coincidan los archivos que se quiere compartir. En el equipo del compañero basta trabajar en `codigo_definitivo` dentro de su clon del repositorio.

No confundir el main.py de la raíz del repositorio con el de esta carpeta. Para esta etapa, ejecutar el de `codigo_definitivo`. No subir modificaciones del proyecto antiguo por accidente.

## 10. Cómo retomar con la IA

Primero leer este documento y los tres archivos Python actuales. Explicar brevemente que completamos S6-P08 y que sigue P09. Si el compañero quiere ponerse al día, repasar los pasos anteriores con los ejemplos existentes antes de avanzar. Si quiere continuar, hacer solo el ejercicio de independencia entre dos objetos, explicarlo y verificar que cambiar uno conserva los datos del otro.

Este archivo comunica el contexto del equipo. Las nuevas indicaciones del usuario y los cambios reales en los archivos pueden actualizarlo; no debe tratarse como autorización para publicar, borrar o avanzar automáticamente sin un pedido correspondiente.
