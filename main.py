import flet as ft

from data.database_manager import DatabaseManager
from ui.app_view import AppView


def main(page: ft.Page) -> None:
    db = DatabaseManager("la_buena_mesa.db")
    db.crear_tablas()
    AppView(page, db).construir()


if __name__ == "__main__":
    ft.app(target=main)
