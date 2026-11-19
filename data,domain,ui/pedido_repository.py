import sqlite3

from domain.pedido import DetallePedido, Pedido
from data.repositorio_base import RepositorioBase


class PedidoRepository(RepositorioBase):

    def agregar(self, pedido: Pedido) -> bool:
        """Guarda el pedido y sus detalles en una sola transaccion."""
        self.ultimo_error = ""
        if len(pedido) == 0:
            self.ultimo_error = "El pedido no tiene platos."
            return False
        try:
            with self.db as cursor:
                cursor.execute(
                    "INSERT INTO pedidos (fecha, cliente, pagado) VALUES (?, ?, ?);",
                    (pedido.fecha, pedido.cliente, int(pedido.pagado)),
                )
                pedido.id = cursor.lastrowid
                cursor.executemany(
                    "INSERT INTO detalles_pedido "
                    "(id_pedido, id_plato, cantidad, precio_unitario) VALUES (?, ?, ?, ?);",
                    [
                        (pedido.id, d.id_plato, d.cantidad, d.precio_unitario)
                        for d in pedido.detalles
                    ],
                )
            return True
        except sqlite3.IntegrityError:
            self.ultimo_error = "Alguno de los platos del pedido ya no existe."
            return False
        except sqlite3.Error as err:
            self.ultimo_error = f"Error de base de datos: {err}"
            return False

    def obtener_todos(self) -> list[Pedido]:
        filas = self._leer(
            "SELECT id, fecha, cliente, pagado FROM pedidos ORDER BY fecha DESC, id DESC;"
        )
        pedidos = []
        for fila in filas:
            pedido = Pedido.desde_tupla(fila)
            detalles = self._leer(
                "SELECT d.id_plato, p.nombre, d.cantidad, d.precio_unitario "
                "FROM detalles_pedido d JOIN platos p ON p.id = d.id_plato "
                "WHERE d.id_pedido = ?;",
                (pedido.id,),
            )
            for d in detalles:
                pedido.agregar_detalle(DetallePedido.desde_tupla(d))
            pedidos.append(pedido)
        return pedidos

    def cambiar_pago(self, id_pedido: int, pagado: bool) -> bool:
        return self._escribir(
            "UPDATE pedidos SET pagado = ? WHERE id = ?;", (int(pagado), id_pedido)
        )

    def eliminar(self, id_registro: int) -> bool:
        # Los detalles se borran solos por ON DELETE CASCADE
        return self._escribir("DELETE FROM pedidos WHERE id = ?;", (id_registro,))

    def total_cobrado(self) -> float:
        return self._escalar(
            "SELECT COALESCE(SUM(d.cantidad * d.precio_unitario), 0) "
            "FROM detalles_pedido d JOIN pedidos p ON p.id = d.id_pedido "
            "WHERE p.pagado = 1;"
        )

    def total_por_cobrar(self) -> float:
        return self._escalar(
            "SELECT COALESCE(SUM(d.cantidad * d.precio_unitario), 0) "
            "FROM detalles_pedido d JOIN pedidos p ON p.id = d.id_pedido "
            "WHERE p.pagado = 0;"
        )
