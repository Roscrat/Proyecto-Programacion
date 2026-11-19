import sqlite3
from typing import Optional


ESQUEMA = """
CREATE TABLE IF NOT EXISTS categorias_gasto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    monto REAL NOT NULL CHECK(monto >= 0),
    fecha TEXT NOT NULL,
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias_gasto(id)
);

CREATE TABLE IF NOT EXISTS platos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL COLLATE NOCASE,
    precio REAL NOT NULL CHECK(precio >= 0)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    cliente TEXT NOT NULL,
    pagado INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS detalles_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    id_plato INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_plato) REFERENCES platos(id)
);

CREATE TABLE IF NOT EXISTS aportes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    monto REAL NOT NULL CHECK(monto >= 0),
    fecha TEXT NOT NULL
);

INSERT OR IGNORE INTO categorias_gasto (nombre) VALUES
    ('Alimentos'), ('Gas'), ('Servicios'), ('Personal'), ('Otros');
"""


class DatabaseManager:
    """Abre la conexion, entrega un cursor y al salir decide entre commit y rollback."""

    def __init__(self, db_path: str = "restaurante.db") -> None:
        self.db_path: str = db_path
        self.__connection: Optional[sqlite3.Connection] = None
        self.__cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        self.__connection = sqlite3.connect(self.db_path)
        self.__connection.execute("PRAGMA foreign_keys = ON;")
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> bool:
        if self.__connection:
            if exc_type is not None:
                self.__connection.rollback()
            else:
                self.__connection.commit()
            if self.__cursor:
                self.__cursor.close()
            self.__connection.close()
        # No se silencian las excepciones, las maneja quien llama
        return False

    def crear_tablas(self) -> None:
        with self as cursor:
            cursor.executescript(ESQUEMA)
