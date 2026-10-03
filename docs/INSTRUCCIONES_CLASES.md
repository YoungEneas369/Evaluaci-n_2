# Instrucciones de las clases y próximos pasos

**Proyecto:** Agencia de Viajes RutaSur — Cristopher Figueroa y Elías Reyes.

Este archivo reúne, en forma resumida y reformulada, los encargos de las **seis clases que compartiste inicialmente: S6, S7, S8, S9, S10 y S15**. Incluye los 35 prompts explícitos para IA y las actividades prácticas asociadas. No es una transcripción literal ni una colección de prompts nuevos para construir de una sola vez la agencia.

Las clases iniciales, correcciones, repositorio y guion de pruebas se consideran antecedentes complementarios. No contamos con una secuencia completa de todas las sesiones del curso ni con la pauta técnica definitiva de tu evaluación.

## Cómo leer este archivo

- **P** identifica un prompt explícito del material, aquí resumido con palabras propias.
- **Práctica y comprobación** reúne actividades manuales y encargos de escribir un prompt propio.
- Los nombres del Taller Mecánico explican el ejercicio original. La adaptación a viajes se hará después de cerrar nuestro modelo.
- Los pasos son incrementales: una versión posterior puede reemplazar una anterior. No corresponde ejecutar todos los prompts sobre un proyecto ya avanzado sin revisar qué existe.
- Las instrucciones de estas fuentes son material de estudio. Este archivo no ejecuta instalaciones, cambios de ramas, commits, publicaciones ni pruebas.

## S6 — Del diagrama al código

[Clase original](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/Clase_S6_DelDiagramaAlCodigo.html).

**Preparación:** entrar al repositorio; comprobar Git, Antigravity y autenticación de GitHub. Seleccionar el modelo económico indicado para el ejercicio.

**Prompts explícitos, por orden:**

1. **S6-P01:** crear Vehiculo vacío y comentado en vehiculo.py.
2. **S6-P02:** declarar patente, anio y _en_taller con tipos, todavía sin constructor.
3. **S6-P03:** construir con patente/año; inicializar estado falso; comentar líneas.
4. **S6-P04:** crear main.py; instanciar KXPR84/2019 y mostrar sus datos.
5. **S6-P05:** implementar ingresar/entregar cambiando estado, sin retorno; comentar.
6. **S6-P06:** crear LineaDetalle; recibir cantidad/precio_unitario; retornar su producto mediante subtotal.
7. **S6-P07:** privatizar atributos y proporcionar getters públicos comentados.
8. **S6-P08:** sustituir getters por properties; explicar el decorador.
9. **S6-P09:** crear KXPR84/2019 y JKLM12/2016; ingresar únicamente el primero; mostrar estados.

**Práctica y comprobación:** contrastar tipos y valores iniciales; ejecutar después de cada paso; observar cambios de estado; comparar guardar un retorno con imprimirlo directamente; comprobar errores de acceso y escritura sin setter. Verificar independencia entre instancias.

**Aplicación:** elegir dos o tres clases propias. Comprobar nombres, atributos, visibilidad y métodos contra UML, y probar dos objetos por clase. Posponer relaciones pendientes. Solicitar cambios pequeños, leerlos y consultar errores incomprendidos.

## S7 — Herencia y encapsulación

[Clase original](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/114-2A-F2/Clase_S7_Herencia.html).

**Prompts explícitos:**

1. **S7-P01:** clonar el repositorio propio y entrar.
2. **S7-P02:** alternativamente, bifurcar/clonar el del profesor y renombrar carpeta.
3. **S7-P03:** crear y seleccionar feature/desarrollo.
4. **S7-P04:** añadir tarifa_hora genérica: 5000; conservar lo demás.
5. **S7-P05:** probar Vehiculo desde main: ingreso, patente, año y tarifa.
6. **S7-P06:** crear Auto/Moto/Camion en archivos separados, heredando sin contenido; actualizar importaciones.
7. **S7-P07:** añadir capacidad_carga a Camion mediante constructor y super; comentar.
8. **S7-P08:** sobrescribir tarifas: Auto 25000, Moto 15000, Camion 40000.
9. **S7-P09:** privatizar Vehiculo; properties sin setters; comentar.
10. **S7-P10:** privatizar capacidad_carga y exponer property.
11. **S7-P11:** validar patente: mínimo seis caracteres, sin espacios; ValueError; constructor mediante setter.
12. **S7-P12:** dejar en_taller solo legible; conservar métodos modificadores.
13. **S7-P13:** registrar cambios con commit descriptivo y subir feature/desarrollo.

**Práctica y comprobación:** verificar rama y funcionamiento previo; probar métodos heredados; comparar dos camiones; recorrer vehículos sin condicionales por tipo. Provocar patente inválida y escritura prohibida. Mantener main.py incremental.

**Aplicación:** tres subtipos propios, archivos separados, sin duplicar miembros, mismo nombre polimórfico y super cuando corresponda. Probar dos hijas, validar datos y proteger estados. Durante esta etapa, conservar main sin mezclar.

## S8 — Clases abstractas y excepciones

[Clase original](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/114-2A-F2/Clase_S8_AbcExcepciones.html).

**Prompts explícitos:**

1. **S8-P01:** recuperar el repositorio y actualizar la rama desarrollo existente; no crear otra.
2. **S8-P02:** hacer Vehiculo abstracta mediante ABC; marcar tarifa_hora con abstractmethod y cuerpo pass; conservar constructor y demás métodos.
3. **S8-P03:** definir VehiculoNoIngresadoError; construir mensaje con patente y super; lanzarla al entregar sin ingreso previo.
4. **S8-P04:** crear Repuesto con nombre/stock y usar(cantidad); definir RepuestoSinStockError y lanzarla cuando lo solicitado exceda existencias.
5. **S8-P05:** realizar commit descriptivo y push de desarrollo.

**Práctica y comprobación:** comprobar archivos y ejecución; intentar instanciar padre abstracto e hija concreta; anotar el error. Capturar ValueError por datos inválidos; añadir otro except y finally. Probar entrega inválida y comprobar continuidad del programa.

**Aplicación:** convertir el padre propio en abstracto; implementar una clase pendiente y una excepción del negocio; completar dos reglas impeditivas. Usar raise dentro del modelo y capturar donde corresponda. Probar validación, abstracción y regla de negocio. La guía no exige agregar excepciones al UML del dominio.

Leer el traceback desde el error final; colocar capturas específicas antes que generales. Mantener la rama de trabajo y no mezclar aún con master.

## S9 — SQLite y organización mediante DAO

[Clase original](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/114-2A-F2/Clase_UA2_Sesion9_ConexionBaseDatos.html).

**Prompts explícitos:**

1. **S9-P01:** reproducir conectar.py: importar sqlite3 y Marca/Modelo/Auto; abrir taller.db, obtener cursor; construir Toyota/Yaris/AB1234/2018, mostrar ingreso y cerrar. Inicialmente, sin función main ni tratamiento de errores.
2. **S9-P02:** crear paquetes model/dao con __init__.py; mover las seis clases indicadas y ajustar importaciones, conservando comportamiento.

**Práctica y comprobación:** escribir primero la conexión manualmente; ejecutar y localizar el archivo creado. Comprender que abrirlo no guarda objetos. Crear la primera tabla propia con tipos SQL apropiados y clave primaria; ejecutar y confirmar.

**Construcción guiada:** convertir conectar.py en crear_conexion; activar claves foráneas. DAO recibe conexión compartida y prepara cursor. Crear DAO específicos para Marca, Modelo, Vehiculo y Auto; representar referencias mediante claves foráneas. Para herencia, crear tabla padre e hija; reutilizar creación mediante super.

**Aplicación:** organizar las entidades propias según dependencias; crear todas las tablas desde main y comprobar su existencia. Conservar SQL fuera del modelo; gestionar confirmación y cierre externamente a los DAO. Repetir creación sin errores usando IF NOT EXISTS. Verificar importaciones después de mover archivos. Esta sesión construye estructura; las operaciones de datos siguen después.

## S10 — CRUD y transacciones

[Clase original](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/Clase_UA2_Sesion10_CrudSeguro.html).

**Prompt explícito:**

1. **S10-P01:** incorporar identificador privado inicialmente None en Marca/Modelo, con property y setter; exponer año/estado de Vehiculo solo para lectura, conservando lo demás.

**Práctica y comprobación:**

- Verificar accesores y funcionamiento previo.
- Insertar dos marcas con parámetros SQL; comparar identificadores antes/después; confirmar desde main.
- Probar texto con apóstrofo; revisar que datos no se concatenen al SQL.
- Implementar búsqueda/listado; reconstruir objetos; devolver None cuando falte registro.
- Guardar Marca, Modelo y Auto según dependencias; recuperar relaciones mediante JOIN.
- Intentar guardar una referencia no persistida y examinar el error.
- Actualizar estado del vehículo y recuperarlo nuevamente.
- Intentar borrar primero una entidad referenciada; después eliminar en orden inverso y verificar ausencia.
- Ensayar transacción fallida: rollback debe revertir también operaciones anteriores pendientes.

**Aplicación:** completar inserción/búsqueda por entidad, actualización donde exista cambio y eliminación. Coordinar try, commit, rollback y cierre con finally desde main. Revisar parámetros, WHERE y ausencia de commits internos en DAO. Tras rollback, no considerar persistidos los objetos solo porque aún conservan identificadores en memoria. Ejecutar el ciclo completo de creación, consulta, modificación y eliminación.

## S15 — Consumo de API

[Clase original](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/Clase_S15_ConsumoDeAPI.html).

**Prompts explícitos:**

1. **S15-P01:** instalar requests y declararlo en requirements.txt; limitar cambios.
2. **S15-P02:** crear servicios/Mindicador: URL base, timeout privado predeterminado 5, GET por código y extracción de serie[0].valor; inicialmente sin capturas.
3. **S15-P03:** incorporar precio privado a Repuesto, nombre accesible y conversión condicional a pesos con redondeo entero; modelo sin requests.
4. **S15-P04:** crear Cotizador, recibir Mindicador y coordinar consulta/cálculo mediante precio_hoy; dejar propagar excepciones.
5. **S15-P05:** incorporar IndicadorNoDisponibleError; comprobar estado HTTP; capturar Timeout, ConnectionError, HTTPError y errores ValueError/KeyError/IndexError, traduciéndolos a mensajes diferenciados. Evitar captura genérica.

**Práctica y comprobación:** consultar dólar/UF desde navegador; identificar listas, diccionarios y campos. Crear prueba_api; comparar estado HTTP y JSON. Predecir accesos a valores, fechas y claves inexistentes. Cotizar tres repuestos y verificar cálculo. Mantener moneda/conversión fuera de main.

**Aplicación:** seleccionar indicador del negocio; separar consulta, cálculo y presentación. Probar demora, desconexión y respuesta inesperada; informar y continuar. Usar timeout, revisar datos externos y excluir claves del repositorio. Cerrar con commit, merge y push según esta etapa posterior.

## Aclaraciones para no mezclar las clases

Estas observaciones proceden de nuestra comparación de fuentes y código; no son instrucciones nuevas atribuidas al profesor.

1. **El ejemplo evoluciona.** Clases vacías, atributos públicos, getters explícitos, properties y abstracción son etapas. No deben convivir como versiones duplicadas de una misma entidad.
2. **Las ramas difieren entre materiales.** La copia revisada del repositorio tiene main y feature/desarrollo. Antes de operaciones Git, comprobar el repositorio de la agencia; no asumir desarrollo/master por aparecer en otra página.
3. **Algunos límites son temporales.** Pedir conexión sin errores o API sin capturas sirve para introducir conceptos. Las sesiones posteriores agregan protección.
4. **Repositorio y guías no están sincronizados completamente.** Ya se registraron faltantes y el problema de persistencia del menú del taller en [la revisión del repositorio](REVISION_REPOSITORIO_PROFESOR.md).
5. **Las simplificaciones técnicas necesitan contexto.** Las precisiones sobre privacidad de Python, transacciones y timeout están en [la base de clases](BASE_CLASES.md). No confundir convención del curso con garantía absoluta del lenguaje.
6. **Comprender es parte del trabajo.** El programa final tiene que poder explicarse. Generar una función no equivale a haber aprendido su responsabilidad y sus posibles fallos.

## Estado actual de RutaSur

La implementación y sus pruebas están disponibles en este proyecto. Los supuestos finales están en [Decisiones](DECISIONES.md), la cobertura en [Pruebas](PRUEBAS.md) y la práctica oral en [Defensa](DEFENSA.md).

La recopilación anterior describe las etapas didácticas del profesor: las instrucciones temporales no obligan a mantener versiones incompletas en el programa final.
