# Revisión del repositorio guía

Fecha de revisión: 2 de octubre de 2026 (America/Santiago).

Fuente: [taller-mecanico-114-2A-f2](https://github.com/michaelarjelm/taller-mecanico-114-2A-f2).

Copia local: `referencias_profesor/taller-mecanico-114-2A-f2`. Se conservó el código sin modificaciones. El proyecto del estudiante es de **Agencias de Viajes**, pendiente de recibir junto con su diagrama y pauta.

## Versión verificada

- Rama predeterminada: `main`.
- Rama remota adicional: `feature/desarrollo`.
- Ambas apuntan a `8ec1492083fb1b3f0268332adce97f73e96324a9` en la descarga revisada.
- Último commit: 30 de septiembre de 2026; incorpora fecha opcional a la consulta del indicador.
- No se encontraron archivos AGENTS.md en la copia descargada.
- El README solo documenta avances de agosto; el código es posterior. No usar su bitácora como inventario completo del estado actual.

## Organización real

- `model/`: 13 clases. Vehiculo con Auto, Moto y Camion; Marca y Modelo; Persona, Cliente, Usuario y Rol; Repuesto, LineaDetalle y OrdenTrabajo.
- `dao/`: clase DAO base, MarcaDAO, ModeloDAO, VehiculoDAO y AutoDAO.
- `conectar.py`: conexión SQLite y activación de claves foráneas.
- `servicios/miinidicador.py`: clase MiIndicador y método obtener_valor(codigo, fecha=None). Conservar el nombre real al leer el ejemplo: difiere de la guía.
- `main.py`: menú de marcas y cotización de repuestos; no demuestra todos los objetos del modelo.
- `prueba_api.py`: consulta de demostración. No es una suite de pruebas.
- `requirements.txt`: Requests y dependencias fijadas por versión.
- `taller.db`: base incluida en el repositorio; no se modificó ni se utilizó para las comprobaciones.

Relaciones observadas: Modelo referencia Marca; Vehiculo referencia Modelo; Cliente y Usuario referencian Persona; Usuario referencia Rol; OrdenTrabajo referencia Vehiculo y Usuario y contiene una lista de LineaDetalle; cada LineaDetalle referencia Repuesto. Las referencias en código por sí solas no prueban todas las multiplicidades ni las reglas de composición UML: contrastar con el diagrama original.

## Coincidencias y diferencias con las clases

| Tema | Estado del repositorio revisado |
|---|---|
| Herencia y polimorfismo | Auto, Moto y Camion sobrescriben tarifa_hora(). |
| Abstracción | Vehiculo no usa ABC ni abstractmethod; sigue siendo instanciable. |
| Encapsulación | Vehiculo utiliza __en_taller y properties. Auto además exige capacidad_maletero, ausente del constructor simplificado de la guía. |
| Validaciones | Patente valida longitud y espacio simple mediante setter; las demás reglas requieren revisión según el negocio. |
| Excepciones propias | No hay excepciones.py. entregar() devuelve mensajes; Repuesto no tiene usar() ni excepción de stock. |
| Persistencia | Las tablas usan nombres singulares: marca, modelo, vehiculo y auto. |
| CRUD | Solo MarcaDAO tiene las operaciones CRUD. Los otros DAO se limitan a crear tablas. Modelo todavía no tiene id. |
| Transacciones | insertar() no confirma; actualizar() y eliminar() sí confirman dentro de MarcaDAO. Contradice la coordinación externa enseñada en S10. |
| API | Hay timeout y control de serie vacía, pero no raise_for_status(), traducción a excepción propia ni Cotizador separado. main.py coordina directamente el dólar y el cálculo. |
| Autenticación | Usuario.autenticar() retorna True siempre. El nombre password_hash no implica que haya hashing o verificación implementados. |
| Reglas pendientes | Cliente.tiene_deuda() retorna False siempre. OrdenTrabajo ignora intentos de agregar datos cuando está cerrada; no lanza excepción. |

## Comprobaciones ejecutadas

Se revisó la sintaxis con ast.parse de los 25 archivos Python, sin errores. Esto no demuestra que todos los flujos funcionen.

Se importaron únicamente clases locales previamente leídas, evitando archivos de bytecode, y se usó una base temporal separada para reproducir la secuencia del menú:

1. Crear tabla y confirmar.
2. Insertar una marca mediante MarcaDAO.insertar().
3. Leer: aparece una marca en la misma conexión.
4. Cerrar sin otra confirmación y volver a abrir: aparecen cero marcas.

**Resultado:** crear una marca y salir del menú puede perder el registro aunque se haya mostrado un mensaje de éxito. Una actualización o eliminación posterior puede confirmar también inserciones anteriores pendientes, porque comparte la conexión. No copiar esta gestión de transacciones a Agencias de Viajes.

También se comprobó que Vehiculo puede instanciarse, entregar sin ingreso devuelve un mensaje, Modelo no tiene id y Usuario.autenticar() devuelve True sin verificar credenciales.

No se ejecutó el menú interactivo completo, no se consultó la API en vivo y no se instalaron dependencias. Su disponibilidad y respuestas actuales quedan sin verificar. No se alteró ni publicó contenido en GitHub.

## Uso posterior para Agencias de Viajes

Tomar como referencia la separación de responsabilidades, herencia, properties, DAO y consultas parametrizadas. Las entidades y reglas concretas deben salir del proyecto del estudiante, no de reemplazar nombres del taller mecánicamente.

Antes de implementar: recibir proyecto, diagrama y rúbrica; mapear cada requisito al diseño de la agencia; resolver si las diferencias del repositorio son avances pendientes o cambios expresamente exigidos. Las guías y el repositorio no constituyen por sí solos una especificación final coherente.
