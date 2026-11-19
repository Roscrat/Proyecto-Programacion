from domain.gasto import Gasto
from data.repositorio_base import RepositorioBase


class GastoDAO(RepositorioBase):

    def agregar(self, gasto: Gasto) -> bool:
        ok = self._escribir(
            "INSERT INTO gastos (descripcion, monto, fecha, id_categoria) VALUES (?, ?, ?, ?);",
            (gasto.descripcion, gasto.monto, gasto.fecha, gasto.id_categoria),
            "La categoria elegida no existe.",
        )
        if ok:
            gasto.id = self.ultimo_id
        return ok

    def obtener_todos(self) -> list[Gasto]:
        filas = self._leer(
            "SELECT g.id, g.descripcion, g.monto, g.fecha, g.id_categoria, c.nombre "
            "FROM gastos g JOIN categorias_gasto c ON c.id = g.id_categoria "
            "ORDER BY g.fecha DESC, g.id DESC;"
        )
        return [Gasto.desde_tupla(f) for f in filas]

    def actualizar(self, gasto: Gasto) -> bool:
        return self._escribir(
            "UPDATE gastos SET descripcion = ?, monto = ?, fecha = ?, id_categoria = ? "
            "WHERE id = ?;",
            (gasto.descripcion, gasto.monto, gasto.fecha, gasto.id_categoria, gasto.id),
            "La categoria elegida no existe.",
        )

    def eliminar(self, id_registro: int) -> bool:
        return self._escribir("DELETE FROM gastos WHERE id = ?;", (id_registro,))

    def total(self) -> float:
        return self._escalar("SELECT COALESCE(SUM(monto), 0) FROM gastos;")

    def total_por_categoria(self) -> list[tuple[str, float]]:
        return self._leer(
            "SELECT c.nombre, SUM(g.monto) FROM gastos g "
            "JOIN categorias_gasto c ON c.id = g.id_categoria "
            "GROUP BY c.nombre ORDER BY SUM(g.monto) DESC;"
        )
