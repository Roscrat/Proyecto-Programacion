from domain.aporte import Aporte
from data.repositorio_base import RepositorioBase


class AporteDAO(RepositorioBase):

    def agregar(self, aporte: Aporte) -> bool:
        ok = self._escribir(
            "INSERT INTO aportes (descripcion, monto, fecha) VALUES (?, ?, ?);",
            (aporte.descripcion, aporte.monto, aporte.fecha),
        )
        if ok:
            aporte.id = self.ultimo_id
        return ok

    def obtener_todos(self) -> list[Aporte]:
        filas = self._leer(
            "SELECT id, descripcion, monto, fecha FROM aportes ORDER BY fecha DESC, id DESC;"
        )
        return [Aporte.desde_tupla(f) for f in filas]

    def eliminar(self, id_registro: int) -> bool:
        return self._escribir("DELETE FROM aportes WHERE id = ?;", (id_registro,))

    def total(self) -> float:
        return self._escalar("SELECT COALESCE(SUM(monto), 0) FROM aportes;")
