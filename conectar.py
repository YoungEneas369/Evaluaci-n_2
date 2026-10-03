"""Único punto que abre SQLite; la base no depende del directorio de ejecución."""
from pathlib import Path
import sqlite3


def crear_conexion(ruta=None):
    if ruta is None:
        ruta = Path(__file__).resolve().parent / 'data' / 'rutasur.db'
        ruta.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(str(ruta), timeout=5)
    conexion.row_factory = sqlite3.Row
    conexion.execute('PRAGMA foreign_keys = ON')
    return conexion
