from domain.categoria import Categoria
from data.repositorio_base import RepositorioBase


class CategoriaDAO(RepositorioBase):

    def agregar(self, categoria: Categoria) -> bool:
        ok = self._escribir(
            "INSERT INTO categorias_gasto (nombre) VALUES (?);",
            (categoria.nombre,),
            "Ya existe una categoria con ese nombre.",
        )
        if ok:
            categoria.id = self.ultimo_id
        return ok

    def obtener_todos(self) -> list[Categoria]:
        filas = self._leer("SELECT id, nombre FROM categorias_gasto ORDER BY nombre;")
        return [Categoria.desde_tupla(f) for f in filas]

    def eliminar(self, id_registro: int) -> bool:
        return self._escribir(
            "DELETE FROM categorias_gasto WHERE id = ?;",
            (id_registro,),
            "No se puede borrar: la categoria tiene gastos registrados.",
        )
