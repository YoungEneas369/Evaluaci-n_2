# RutaSur: paso a paso de lo que hemos construido

Actualizado: 4 de octubre de 2026. Completamos S6 y comenzamos S7; consultar el paso 11 para el estado vigente.

Esta guía explica la evolución del código. Los fragmentos de los primeros pasos son versiones anteriores para estudiar: no hay que agregarlos junto a las versiones actuales. Los archivos Python contienen la versión vigente.

## 1. Crear una clase vacía (S6-P01)

El profesor empezó con Vehiculo; nosotros usamos Cliente, la persona que compra un viaje.

```python
class Cliente:
    pass
```

`class` declara la clase. Cliente es su nombre, elegido por nosotros. La sangría indica qué pertenece a la clase. `pass` permite dejar su cuerpo pendiente sin error. Un comentario que empieza con `#` explica algo al lector y no se ejecuta.

## 2. Declarar atributos y tipos (S6-P02)

```python
class Cliente:
    nombre: str
    correo: str
    telefono: str
```

Los atributos describen los datos de cada cliente. `str` indica que esperamos texto; estas anotaciones todavía no asignan valores. El teléfono es texto porque puede tener un signo + o ceros iniciales y no se usa para calcular. Quitamos pass porque ya había declaraciones, no porque ya existieran métodos.

## 3. Agregar el constructor (S6-P03)

```python
def __init__(self, nombre_recibido: str, correo_recibido: str, telefono_recibido: str):
    self.nombre = nombre_recibido
    self.correo = correo_recibido
    self.telefono = telefono_recibido
```

Este fragmento va dentro de Cliente. Inicializar significa dejar al objeto con sus valores iniciales. Python llama a __init__ al crear el objeto. `self` se refiere a ese objeto; los otros parámetros reciben los datos que entregamos al llamar a Cliente.

En `self.nombre = nombre_recibido`, se obtiene el valor de la derecha y se guarda en el atributo de la izquierda. El parámetro y el atributo son distintos. Usamos el sufijo recibido para hacer esa diferencia visible; no es una exigencia de Python.

## 4. Crear objetos desde main.py (S6-P04)

```python
from cliente import Cliente

cliente_ana = Cliente("Ana", "ana@example.com", "+56912345678")
print(cliente_ana.nombre)
```

`from cliente import Cliente` trae la clase desde cliente.py. La llamada crea un objeto, el constructor guarda sus datos y la variable cliente_ana permite acceder a él. Después print muestra el nombre. Crear un objeto no imprime automáticamente sus datos.

El estudiante añadió un segundo cliente por iniciativa propia. Sus comentarios y ejemplos se conservaron.

## 5. Agregar métodos que cambian datos (S6-P05)

El profesor modificaba el estado de un vehículo. Adaptamos el ejercicio a cambiar datos de contacto:

```python
def cambiar_correo(self, correo_nuevo: str) -> None:
    self.correo = correo_nuevo
```

Se usa así:

```python
cliente_ana.cambiar_correo("ana.nuevo@example.com")
```

El parámetro correo_nuevo recibe el texto y self se refiere a cliente_ana. La asignación cambia el correo de ese objeto. También agregamos cambiar_telefono y el estudiante añadió cambiar_nombre.

`-> None` indica que no esperamos un resultado útil de retorno. No significa por sí solo que el método cambie datos: lo que modifica el objeto es la asignación de su cuerpo.

## 6. Calcular y retornar un resultado (S6-P06)

El profesor calcula cantidad por precio en LineaDetalle. Usamos PaqueteNacional y precio por viajero para mantener los servicios incluidos sin cobrarlos otra vez.

```python
def calcular_total(self, cantidad_viajeros: int) -> float:
    return cantidad_viajeros * self.precio_por_viajero
```

Con precio 150000 y cantidad 2, el resultado es 300000:

```python
total_viaje = paquete_sur.calcular_total(2)
print(total_viaje)
```

`return` entrega el resultado de la multiplicación. `=` lo asigna a total_viaje. `print` lo muestra. Son tres acciones diferentes. Las anotaciones int y float no convierten ni validan automáticamente los valores.

El archivo se llama paquetesAgencia.py. El estudiante ensayó también internacional y crucero, pero pidió retirarlos para seguir en orden. Volverán en la etapa de herencia; su cálculo requerirá tipo de cambio y el crucero una fórmula propia aún por definir.

## 7. Atributos privados y getters (S6-P07)

Cambiamos los accesos internos de nombre a __nombre, y de igual manera los demás atributos. Añadimos métodos públicos para leerlos:

```python
def get_nombre(self) -> str:
    return self.__nombre
```

`get` es una convención de nombre que significa obtener; Python no la exige. Podríamos llamar al método obtener_nombre. `def` define el método y `return` entrega el valor.

```python
nombre_obtenido = cliente_ana.get_nombre()
```

El método consulta el nombre ya guardado, no crea al cliente ni vuelve a pedir el nombre. Los dos guiones bajos provocan un cambio interno de nombre para evitar accesos accidentales; no son una barrera de seguridad absoluta.

## 8. Reemplazar getters por propiedades (S6-P08)

```python
@property
def nombre(self) -> str:
    return self.__nombre
```

Renombramos nosotros get_nombre a nombre. El decorador @property no quita get_ automáticamente: permite ejecutar la lectura al consultar la propiedad sin paréntesis.

```python
print(cliente_ana.nombre)
```

El dato sigue guardado en self.__nombre. La propiedad pública se llama nombre. Como no definimos un setter, `cliente_ana.nombre = "Otra persona"` produce AttributeError. Para cambiarlo usamos cambiar_nombre.

Aplicamos propiedades a Cliente y PaqueteNacional. Los métodos cambiar_... y calcular_total siguen llamándose con paréntesis: no los convertimos en propiedades. Se comprobó lectura, cambio mediante método y rechazo de asignación directa a nombre.

## 9. Comprobar independencia entre objetos (S6-P09)

```python
cliente_lucia = Cliente("Lucía", "lucia@example.com", "+56911111111")
cliente_diego = Cliente("Diego", "diego@example.com", "+56922222222")
cliente_lucia.cambiar_correo("lucia.nuevo@example.com")
print(cliente_lucia.correo)
print(cliente_diego.correo)
```

El resultado es lucia.nuevo@example.com para Lucía y diego@example.com para Diego. Cada llamada a Cliente crea un objeto distinto. Durante la llamada de Lucía, self representa a Lucía; Diego conserva sus datos. main.py muestra ambos antes y después. Se ejecutó y verificó ese resultado.

## 10. Estado actual y siguiente clase

Los archivos actuales usan atributos privados y properties, conservan métodos para modificar datos y calculan el total del paquete nacional. Ejecutar `python main.py` desde codigo_definitivo. No hay dependencias externas en esta etapa.

Sigue S7. El material empieza por preparar el repositorio y la rama feature/desarrollo; después añade comportamiento común, lo prueba y recién entonces crea clases hijas. Antes de modificar código, revisar el estado Git y la rama, sin duplicar repositorios ni mezclar cambios del proyecto anterior.

Para RutaSur necesitaremos una clase general Paquete antes de conectar las especializaciones. PaqueteNacional será un tipo de Paquete. Eso se llama herencia. La API no corresponde a este primer paso: la estudiaremos en S15. No generar de una vez todas las clases pendientes.

Para requisitos del negocio, decisiones pendientes y forma de enseñar, leer [Contexto_Evaluación_2.md](Contexto_Evaluación_2.md).

## 11. Preparar S7: rama y clase general

Creamos y seleccionamos feature/desarrollo con git switch -c feature/desarrollo dentro de agencia_viajes. La rama es local: crearla no publica en GitHub ni crea otra carpeta. No es necesario volver a clonar el repositorio ya existente.

Para preparar el comportamiento común antes de crear hijas, renombramos PaqueteNacional a Paquete en paquetesAgencia.py y actualizamos la importación y la creación en main.py. Conservamos constructor, propiedades y calcular_total. No añadimos todavía herencia ni API.

```python
from paquetesAgencia import Paquete
paquete_sur = Paquete("Viaje a Puerto Varas", 150000)
print(paquete_sur.calcular_total(2))
```

El resultado sigue siendo 300000. La adaptación de S7-P04–P05 usa nuestro cálculo común, no la tarifa fija de 5000 del taller del profesor. Las clases nacional, internacional y crucero aparecerán como hijas en el siguiente ejercicio. Esta es una etapa intermedia: Paquete será abstracto cuando lleguemos a S8.


## 12. Herencia, super y métodos propios (S7-P06 a P10)

Se crearon PaqueteNacional, PaqueteInternacional y Crucero en archivos separados heredando de Paquete. Crucero añadió noches mediante constructor propio y super().__init__. Cada hija implementó calcular_total: nacional en CLP; internacional con cambio; crucero con cambio y recargo ilustrativo del 10 %. No hay API todavía. Las noches se guardaron como __noches y se leen con @property.

## 13. Integración del trabajo de Elías

Se incorporaron Persona y la jerarquía de trabajadores. Cliente ahora hereda Persona y requiere nombre, RUT, correo y teléfono. Se separó Viajero con pasaporte; el comprador no lo guarda. Los setters heredados validan nombre/RUT al construir y al modificar. Esta parte llegó por integración urgente y todavía debemos explicarla como siguiente ejercicio de aprendizaje. Ver INTEGRACION_EQUIPO.md para cambios de firmas, origen, límites y pruebas.
