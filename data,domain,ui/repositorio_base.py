from abc import ABC, abstractmethod
import sqlite3
from typing import Any

from data.database_manager import DatabaseManager


class RepositorioBase(ABC):
    """Contrato comun de los DAO y repositorios, con utilidades para ejecutar SQL."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db: DatabaseManager = db
        self.ultimo_error: str = ""
        self.ultimo_id: int = 0

    @abstractmethod
    def agregar(self, entidad: Any) -> bool:
        pass

    @abstractmethod
    def obtener_todos(self) -> list:
        pass

    @abstractmethod
    def eliminar(self, id_registro: int) -> bool:
        pass

    def _escribir(
        self,
        sql: str,
        parametros: tuple,
        mensaje_integridad: str = "El dato esta repetido o no cumple una restriccion.",
    ) -> bool:
        """Ejecuta un INSERT, UPDATE o DELETE parametrizado."""
        self.ultimo_error = ""
        try:
            with self.db as cursor:
                cursor.execute(sql, parametros)
                self.ultimo_id = cursor.lastrowid or 0
                if cursor.rowcount == 0:
                    self.ultimo_error = "No se encontro el registro."
                    return False
            return True
        except sqlite3.IntegrityError:
            self.ultimo_error = mensaje_integridad
            return False
        except sqlite3.Error as err:
            self.ultimo_error = f"Error de base de datos: {err}"
            return False

    def _leer(self, sql: str, parametros: tuple = ()) -> list[tuple]:
        self.ultimo_error = ""
        try:
            with self.db as cursor:
                cursor.execute(sql, parametros)
                return cursor.fetchall()
        except sqlite3.Error as err:
            self.ultimo_error = f"Error de base de datos: {err}"
            return []

    def _escalar(self, sql: str, parametros: tuple = ()) -> float:
        filas = self._leer(sql, parametros)
        return float(filas[0][0]) if filas and filas[0][0] is not None else 0.0
