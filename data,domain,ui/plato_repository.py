from domain.plato import Plato
from data.repositorio_base import RepositorioBase


class PlatoRepository(RepositorioBase):

    def agregar(self, plato: Plato) -> bool:
        ok = self._escribir(
            "INSERT INTO platos (nombre, precio) VALUES (?, ?);",
            (plato.nombre, plato.precio),
            "Ya existe un plato con ese nombre.",
        )
        if ok:
            plato.id = self.ultimo_id
        return ok

    def obtener_todos(self) -> list[Plato]:
        filas = self._leer("SELECT id, nombre, precio FROM platos ORDER BY nombre;")
        return [Plato.desde_tupla(f) for f in filas]

    def actualizar(self, plato: Plato) -> bool:
        return self._escribir(
            "UPDATE platos SET nombre = ?, precio = ? WHERE id = ?;",
            (plato.nombre, plato.precio, plato.id),
            "Ya existe un plato con ese nombre.",
        )

    def eliminar(self, id_registro: int) -> bool:
        return self._escribir(
            "DELETE FROM platos WHERE id = ?;",
            (id_registro,),
            "No se puede borrar: el plato ya aparece en algun pedido.",
        )
