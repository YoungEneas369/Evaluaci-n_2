"""Tablas y restricciones. El SQL permanece en la capa DAO."""


def crear_tablas(conexion):
    conexion.executescript('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY, nombre_usuario TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL, rol TEXT NOT NULL CHECK(rol IN ('agente','administrador')),
            hash_password TEXT NOT NULL, salt TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, correo TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY, nombre TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS paquetes (
            id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, precio_base TEXT NOT NULL,
            proveedor_id INTEGER NOT NULL REFERENCES proveedores(id)
        );
        CREATE TABLE IF NOT EXISTS paquetes_nacionales (
            paquete_id INTEGER PRIMARY KEY REFERENCES paquetes(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS paquetes_internacionales (
            paquete_id INTEGER PRIMARY KEY REFERENCES paquetes(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS cruceros (
            paquete_id INTEGER PRIMARY KEY REFERENCES paquetes(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS disponibilidad (
            proveedor_id INTEGER NOT NULL REFERENCES proveedores(id), fecha TEXT NOT NULL,
            cupos_totales INTEGER NOT NULL CHECK(cupos_totales >= 0),
            cupos_disponibles INTEGER NOT NULL CHECK(cupos_disponibles >= 0 AND cupos_disponibles <= cupos_totales),
            PRIMARY KEY(proveedor_id, fecha)
        );
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id INTEGER PRIMARY KEY, codigo TEXT NOT NULL, valor TEXT NOT NULL,
            fecha_indicador TEXT NOT NULL, consultado_en TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY, cliente_id INTEGER NOT NULL REFERENCES clientes(id),
            paquete_id INTEGER NOT NULL REFERENCES paquetes(id), fecha TEXT NOT NULL,
            precio_unitario INTEGER NOT NULL CHECK(precio_unitario > 0),
            agente_id INTEGER NOT NULL REFERENCES usuarios(id),
            estado TEXT NOT NULL CHECK(estado IN ('pendiente','confirmada','cancelada')),
            cotizacion_id INTEGER REFERENCES cotizaciones(id)
        );
        CREATE TABLE IF NOT EXISTS viajeros (
            id INTEGER PRIMARY KEY, reserva_id INTEGER NOT NULL REFERENCES reservas(id) ON DELETE CASCADE,
            nombre TEXT NOT NULL, pasaporte TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS detalles_reserva (
            id INTEGER PRIMARY KEY, reserva_id INTEGER NOT NULL REFERENCES reservas(id) ON DELETE CASCADE,
            tipo TEXT NOT NULL CHECK(tipo IN ('vuelo','hotel','seguro','excursion')),
            descripcion TEXT NOT NULL, cantidad INTEGER NOT NULL CHECK(cantidad > 0)
        );
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY, reserva_id INTEGER NOT NULL REFERENCES reservas(id),
            monto INTEGER NOT NULL CHECK(monto > 0), administrador_id INTEGER NOT NULL REFERENCES usuarios(id),
            fecha TEXT NOT NULL
        );
    ''')
