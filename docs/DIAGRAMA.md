# Modelo de clases implementado

El diagrama selecciona los atributos y métodos relevantes; las propiedades completas están en `model/`. El signo `-` representa atributos privados y `+` acceso público. Las flechas de triángulo representan herencia; el diamante lleno, composición; el vacío, referencias a objetos que existen independientemente. Las líneas punteadas expresan dependencias de uso. Los objetos persistidos tienen identificador opcional hasta su inserción.

## Personas y permisos

```mermaid
classDiagram
    class Persona {
        -str nombre
        +nombre str
    }
    class Cliente {
        -int id
        -str correo
    }
    class Viajero {
        -str pasaporte
        +validar_pasaporte()
    }
    class Trabajador {
        <<abstract>>
        +rol str
        +puede(accion) bool
    }
    class AgenteViajes {
        +rol str
        +puede(accion) bool
    }
    class Administrador {
        +rol str
        +puede(accion) bool
    }
    class Usuario {
        -int id
        -str nombre_usuario
        -Trabajador trabajador
        +exigir_permiso(accion)
    }
    Persona <|-- Cliente
    Persona <|-- Viajero
    Persona <|-- Trabajador
    Trabajador <|-- AgenteViajes
    Trabajador <|-- Administrador
    Usuario "1" *-- "1" Trabajador : identidad del acceso
```

El administrador no hereda una operación de atención al cliente. `puede` devuelve permisos distintos en cada rol; `Usuario.exigir_permiso` convierte una operación prohibida en excepción. El trabajador de esta versión se reconstruye desde los datos del usuario y no se mantiene como registro independiente.

## Paquetes y reservas

```mermaid
classDiagram
    class Paquete {
        <<abstract>>
        -int id
        -str nombre
        -Decimal precio_base
        -Proveedor proveedor
        +calcular_precio(dolar) int
    }
    class PaqueteNacional {
        +calcular_precio(dolar) int
    }
    class PaqueteInternacional {
        +calcular_precio(dolar) int
    }
    class Crucero {
        +Decimal RECARGO_SERVICIO
        +calcular_precio(dolar) int
    }
    class Proveedor {
        -int id
        -str nombre
    }
    class Disponibilidad {
        -int proveedor_id
        -str fecha
        -int total
        -int disponibles
        +verificar(cantidad)
    }
    class Reserva {
        -int id
        -str fecha
        -str estado
        -int precio_unitario
        -tuple viajeros
        -tuple detalles
        -list pagos
        +total int
        +pagado int
        +registrar_pago(pago)
        +confirmar()
        +cancelar()
    }
    class Cliente
    class Viajero
    class DetalleReserva {
        -str tipo
        -str descripcion
        -int cantidad
    }
    class Pago {
        -int monto
        -int administrador_id
        -str fecha
    }
    class TipoCambio {
        -Decimal valor
        -str fecha
    }
    Paquete <|-- PaqueteNacional
    Paquete <|-- PaqueteInternacional
    Paquete <|-- Crucero
    Paquete "0..*" o-- "1" Proveedor : organizador
    Proveedor "1" *-- "0..*" Disponibilidad : cupos por fecha
    Reserva "0..*" o-- "1" Cliente : comprador
    Reserva "0..*" o-- "1" Paquete : oferta elegida
    Reserva "1" *-- "1..*" Viajero : datos para ese viaje
    Reserva "1" *-- "1..*" DetalleReserva : servicios incluidos
    Reserva "1" *-- "0..*" Pago : abonos
    Reserva ..> TipoCambio : cotizacion_id opcional
```

`Reserva–DetalleReserva` es composición: cada detalle guardado pertenece a una reserva. Aquí también los datos del viajero se guardan por reserva; una persona que viaje nuevamente obtiene otro registro con los datos de ese viaje. `Cliente`, `Paquete` y `Proveedor` son objetos compartidos; no desaparecen al cancelar una reserva. Las agregaciones representan esas referencias compartidas, siguiendo la convención utilizada para referencias entre objetos en las clases del curso.

Disponibilidad pertenece a un proveedor y se identifica por proveedor/fecha. La referencia está en `proveedor_id`; `Proveedor` no mantiene una lista duplicada en memoria. Lo mismo ocurre con el administrador de cada pago y el agente de cada reserva: se guardan identificadores de usuario. La base restringe borrados que dejarían esas referencias sin destino.

## Separación de responsabilidades

```mermaid
flowchart LR
    main[main / Consola] --> Agencia
    main --> Autenticacion
    Agencia --> Modelo[Objetos de model]
    Agencia --> DAO[DAO de entidades]
    DAO --> SQLite[(SQLite)]
    Autenticacion --> UsuarioDAO
    UsuarioDAO --> SQLite
    Agencia --> Cotizador
    Cotizador --> Mindicador
    Cotizador --> Paquete[Paquete.calcular_precio]
    Mindicador --> API[API pública dólar]
```

El polimorfismo ocurre cuando `Cotizador` invoca `paquete.calcular_precio(dolar)`: el objeto concreto decide la fórmula. Seleccionar una clase al crear o reconstruir un paquete no sustituye ese comportamiento polimórfico.
