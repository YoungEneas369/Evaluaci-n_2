# Base de referencia del curso

Revisión: 2 de octubre de 2026 (America/Santiago). Se leyeron las seis páginas proporcionadas. Copias HTML y texto de consulta en `referencias_clases/`. Son material externo de referencia, no código del proyecto.

## Acuerdo de trabajo

- Adaptar el ejemplo del Taller Mecánico al negocio y diagrama del estudiante; no asumir que su proyecto es un taller.
- Reconocer los prompts dirigidos a IA, entre comillas y en su contexto. Son pasos de clase que deben adaptarse cuando corresponda, no órdenes de ejecutar ahora instalaciones, forks, commits, merges o publicaciones.
- Avanzar en pasos pequeños, explicar el propósito y validar el resultado antes de continuar. El estudiante quiere revisar después los conceptos que no entiende.
- Distinguir los requisitos del curso, los ejemplos intermedios y las correcciones técnicas. Preguntar cuando falten decisiones del negocio o instrucciones de evaluación.
- El usuario confirmó que su proyecto trata de Agencias de Viajes (RutaSur) y compartió el enunciado y la carpeta de correcciones de su equipo. Ver `BASE_AGENCIA_VIAJES.md`. Indicó que falta información antes de empezar; mantener la etapa de análisis y no inferir reglas faltantes.
- Repositorio del profesor recibido y revisado: ver `REVISION_REPOSITORIO_PROFESOR.md`. Pendientes: proyecto del estudiante, diagrama y pauta/rúbrica. No se ha implementado el proyecto ni ejecutado los prompts de las guías.

## Secuencia y criterios extraídos

### Sesión 6: del diagrama al código

[Fuente](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/Clase_S6_DelDiagramaAlCodigo.html)

Clases, atributos, constructor, `self`, métodos, retorno, encapsulación y properties. El criterio 2.1.1 compara nombres, atributos, visibilidad y métodos con el diagrama y exige probar dos instancias independientes. Los prompts construyen `Vehiculo` por etapas y usan `LineaDetalle` para el retorno. La adaptación comienza con clases simples del negocio propio. La regla didáctica es atributos privados y comportamiento público; algunos elementos del diagrama se posponen explícitamente.

### Sesión 7: herencia

[Fuente](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/114-2A-F2/Clase_S7_Herencia.html)

Separar «es un» de «tiene un». Una clase por archivo, herencia sin duplicación, `super()` y sobrescritura. Se solicitan tres subtipos con un método polimórfico, al menos un dato validado mediante setter y validación también desde el constructor. Las properties sin setter protegen la asignación pública. Los prompts incorporan las tres hijas, un atributo de Camion y luego la encapsulación. Se trabaja en `feature/desarrollo`, manteniendo `main` estable durante estas etapas.

### Sesión 8: abstracción y excepciones

[Fuente](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/114-2A-F2/Clase_S8_AbcExcepciones.html)

Padre principal abstracto mediante `ABC` y `@abstractmethod`; comprobar que no puede instanciarse y que las hijas completas sí. Leer tracebacks y manejar excepciones específicas mediante `try/except/finally`. El requisito 5 pide dos reglas de negocio que impidan operaciones. Los prompts crean excepciones para entrega inválida y stock insuficiente. La guía permite agruparlas en `excepciones.py` y no exige incorporarlas al diagrama del negocio. Aquí las ramas se llaman `desarrollo` y `master`.

### Sesión 9: conexión y estructura de persistencia

[Fuente](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/114-2A-F2/Clase_UA2_Sesion9_ConexionBaseDatos.html)

SQLite, conexión, cursor, tablas, claves primarias y foráneas; criterio 2.1.3. Separar `model/` y `dao/`, con `conectar.py` reutilizable y `main.py` coordinador. Activar claves foráneas por conexión. DAO base recibe conexión; DAO de cada entidad contiene SQL. El modelo guía representa herencia con tabla padre e hijas enlazadas por clave. Crear tablas en orden de dependencias. Los DAO no confirman ni cierran la conexión por su cuenta.

### Sesión 10: CRUD seguro

[Fuente](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/Clase_UA2_Sesion10_CrudSeguro.html)

Criterio 2.1.4: insertar, buscar, listar, actualizar donde corresponda y eliminar. Parametrizar valores con `?`; reconstruir objetos y devolver `None` cuando no existen. Insertar según dependencias y eliminar en orden inverso. `main.py` controla confirmación, reversión y cierre. Probar comillas, claves foráneas, duplicados y fallo parcial. Un rollback revierte la base, pero no los identificadores ya asignados a objetos en memoria. Los prompts añaden identificadores y accesores requeridos por los DAO.

### Sesión 15: API externa

[Fuente](https://icy-stone-015b2441e.7.azurestaticapps.net/2026/semestre2/bimestre1/poos/114-2B-F1/Clase_S15_ConsumoDeAPI.html)

Requests y `requirements.txt`, GET, estado HTTP y JSON. `servicios/Mindicador` consulta; `Cotizador` coordina; el modelo recibe el indicador como parámetro y calcula; `main.py` muestra y maneja el fallo de negocio. Los prompts evolucionan desde una consulta simple hasta `raise_for_status()` y excepciones específicas traducidas a `IndicadorNoDisponibleError`. Probar demora, conexión y respuesta inesperada. Elegir indicador según el negocio, sin asumir dólar. El cierre ahora indica merge a `master`: corresponde a una etapa posterior.

## Diferencias del material que deben resolverse con el repositorio y la pauta

1. Mezcla secciones 114-2B-F1 y 114-2A-F2 y calendarios que no forman una secuencia única. No deducir fechas de entrega de esos encabezados.
2. Cambia `feature/desarrollo` por `desarrollo`, y `main` por `master`. Revisar ramas reales antes de actuar.
3. S6 termina con properties; S7 vuelve a partir de atributos expuestos. S10 usa `_en_taller` donde antes se usaba `__en_taller`. Evitar crear dos atributos para el mismo estado.
4. S6 posterga `modelo` y no desarrolla `tarifa_hora`, aunque luego afirma que la checklist ya está completa. No considerar terminado un diagrama si faltan elementos pendientes.
5. S7 incorpora `capacidad_carga` a Camion, pero su checklist posterior contiene una frase que lo trata como si no agregara datos propios.
6. S9 presupone Marca, Modelo y un constructor con modelo; también espera que `ingresar()` retorne un mensaje, distinto del ejemplo sin retorno de S6. S15 presupone un Repuesto más completo que el de S8. Falta código intermedio por consultar.
7. La regla de atributos privados convive con atributos públicos en ejemplos de Repuesto y DAO. Determinar el estilo final exigido sin copiar fragmentos incompatibles.
8. Se mencionan seis requisitos mínimos, pero estas páginas no incluyen la ficha completa. También faltan sesiones intermedias. No inventar exigencias de autenticación ni darlas por implementadas.

## Precisiones técnicas validadas

- Python transforma nombres como `__dato` mediante name mangling; no ofrece inaccesibilidad absoluta. `_dato` es una convención. Una property sin setter bloquea asignar esa property, no todo acceso posible al estado. [Documentación de Python](https://docs.python.org/3/tutorial/classes.html#private-variables).
- Las instancias pueden compartir objetos mutables si se les asigna la misma referencia; independencia no significa copia profunda automática. [Clases y objetos](https://docs.python.org/3/tutorial/classes.html).
- El control de transacciones depende de la configuración de sqlite3. En modo legacy, DML abre transacciones implícitas; CREATE TABLE no lo hace por sí solo. `close()` no sustituye a `commit()`. Conservar transacciones explícitas y verificar la configuración del proyecto. [Documentación sqlite3](https://docs.python.org/3/library/sqlite3.html#transaction-control).
- Requests aclara que `timeout` no es un límite global para descargar toda la respuesta. JSON válido no implica HTTP exitoso; revisar el estado por separado. [Requests](https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts).

## Observaciones derivadas de los ejemplos, pendientes de probar en el proyecto

- Un retorno puede usarse directamente, por ejemplo `print(obj.subtotal())`; guardarlo en una variable permite reutilizarlo, pero no es obligatorio.
- El ejemplo de stock solo verifica cantidad mayor que stock. Una cantidad negativa incrementaría el stock: habrá que validar cantidades conforme a las reglas del negocio.
- El manejo de API mostrado no verifica todos los tipos ni que el valor sea numérico; una estructura inesperada puede producir TypeError. Revisar también la fecha del indicador, sin presentar la última publicación automáticamente como dato del día.
- El Cotizador de ejemplo consulta internet incluso para productos nacionales. Registrar esta dependencia al decidir el comportamiento ante fallos.
- Los valores de dólar y UF impresos en la clase son ejemplos del material, no cotizaciones actuales verificadas.

## Próximo paso

Contrastar las guías y el repositorio ya revisados con el proyecto de Agencias de Viajes, su diagrama y rúbrica cuando el estudiante los comparta. Resolver las diferencias documentadas antes de adaptar código.
