# Contexto de Evaluación 2 — versión integrada del equipo

Actualizado: 4 de octubre de 2026. Cristopher Figueroa y Elías Reyes.

## Objetivo actual

El usuario pidió priorizar complementar el trabajo de ambos con correcciones para tener una versión común. Esta integración se hizo antes de continuar el siguiente ejercicio individual. No significa que el estudiante ya comprenda todo lo incorporado.

Repositorio compartido: YoungEneas369/Evaluaci-n_2, rama feature/desarrollo, carpeta codigo_definitivo. Leer README.md, INTEGRACION_EQUIPO.md y los archivos reales antes de editar. No confundir el proyecto anterior de la raíz con esta carpeta.

En el PC de Cristopher se sigue editando C:\Evaluación_2\codigo_definitivo por preferencia del usuario. Existe una copia dentro de C:\Evaluación_2\agencia_viajes\codigo_definitivo para Git. Sincronizar explícitamente al preparar entregas, revisando diferencias. No hay sincronización automática. No modificar otras áreas del repositorio para este aprendizaje.

## Estado del código

Hay Persona; Cliente(Persona); Trabajador(Persona), AgenteViajes(Trabajador) y Administrador(Trabajador); Viajero separado; Paquete con PaqueteNacional, PaqueteInternacional y Crucero. Consultar firmas y responsabilidades en INTEGRACION_EQUIPO.md.

Se completó S6, se practicó S7 hasta herencia, constructor con super, sobrescritura y encapsulamiento del padre y de noches en Crucero (P10). Los setters de Persona llegaron con la integración de Elías. El siguiente paso de aprendizaje es explicar su funcionamiento y adaptación a S7-P11, no pasar de inmediato a base de datos.

Los ejercicios anteriores de PASO_A_PASO.md muestran versiones históricas. En la versión actual, Cliente recibe nombre, rut, correo y telefono; no pasaporte. El antiguo ejemplo de Lucía/Diego fue retirado por el estudiante y permanece como explicación histórica. No restaurarlo sin motivo.

## Forma de enseñar requerida

Seguir el orden del profesor, un cambio pequeño por ejercicio. Antes del código explicar el problema, por qué se hace el cambio y qué otros datos afecta o no. Ante una duda, detener el avance y discutirla. No confundir terminar una integración con haber enseñado sus conceptos.

El estudiante entendió mejor parámetro frente a atributo usando nombre_recibido y self.__nombre. Reforzar:

- Recibir un parámetro no lo guarda como atributo automáticamente.
- La asignación guarda, return entrega un resultado y print lo muestra.
- self es el objeto sobre el que trabaja el método, no otro objeto adicional.
- get es una convención del nombre; def define el método. @property no elimina get_ automáticamente: renombramos el método y permitimos leer sin paréntesis.
- Definir __init__ en la hija hace que se use ese en lugar del heredado. super().__init__ llama al del padre sobre el mismo objeto para inicializar sus datos. Sin constructor propio, la hija utiliza el heredado. No se necesita super para heredar todos los métodos.
- La cantidad de viajeros se recibe en calcular_total; pertenece a una contratación y después a Reserva, no a la oferta Paquete. Guardarla en BD será una decisión de persistencia de la reserva.
- __noches almacena el dato y noches es la propiedad pública de lectura. Asignar noches después de crear el objeto es distinto de crearlo con nombre/precio/noches. No tener setter bloquea la escritura de la propiedad; poner __ no valida valores por sí solo.
- Encapsular permite que la clase administre sus datos mediante operaciones definidas. Un cambio de nombre no cambia correo/precio/noches si el código no lo indica.

El usuario añade comentarios y ejemplos: leerlos y preservarlos siempre que sean compatibles. Los cambios de firmas y cualquier corrección deben explicarse. Mantener contexto y paso a paso actualizados al compartir.

## Requisitos y fuentes

Se conserva la separación comprador/viajero y el pasaporte del viajero indicada por el feedback específico del equipo. Agente arma/vende y atiende; administrador gestiona proveedores/pagos y no atiende. Tres tipos de paquete con fórmulas distintas: nacional CLP, internacional y crucero con cambio. Reserva contiene varios DetalleReserva con TipoItem compartido; proveedor tiene cupos por fecha.

Guion del equipo 114-2A-F2: P01 ejecución/menú; P02-P06 CRUD y persistencia; P07 acepta F12345678; P08 rechaza pasaporte vacío en el flujo internacional; P09-P11 precios; P12-P13 reserva con detalles; P14 anticipo mínimo del 50 %; P15 cupos por proveedor/fecha; P16 dólar de https://mindicador.cl/api/dolar; P17 error de red sin caída; P18 opción inválida; P19 entrada numérica inválida.

Precio por viajero con servicios incluidos: decisión tomada para no cobrar dos veces los detalles. Fórmula del crucero con 10 % sigue siendo didáctica y pendiente de acuerdo definitivo. No se confirma una longitud oficial de pasaporte. Dólar de ejemplo 950 no es real ni respaldo automático ante error. Con API, conservar fecha real de publicación del indicador.

Referencia técnica ES2 de otra sección (114-2B-F1): POO, excepciones, conexión BD, CRUD parametrizado, hash, consulta/deserialización/persistencia de API y defensa. No trasladar calendario o porcentajes ni presentarla como pauta completa confirmada de la sección propia.

## Lo que todavía falta

No hay sistema de reservas ni base de datos, autenticación real, API o control de permisos ejecutando operaciones. Las pruebas de integración no certifican el guion completo. RUT solo no vacío, nombre mínimo dos caracteres por decisión didáctica; aún faltan validaciones de contacto y cantidades/precios/noches. No afirmar que password_hash genera o verifica un hash.

Continuación de clases: S7 setters y validación; S8 abstracción y excepciones; S9 SQLite/modelo/DAO; S10 CRUD y transacciones; S15 API. Al terminar el proyecto, simulación de defensa: una pregunta por vez, respuesta del estudiante primero y retroalimentación después.
