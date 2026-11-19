# Control de gastos y pedidos de un restaurante

Aplicacion de escritorio hecha con Flet y SQLite para llevar las cuentas de un restaurante familiar:
gastos de mercado y servicios, menu con precios, pedidos por dia y dinero disponible.

## Como ejecutarlo

    pip install -r requirements.txt
    python main.py

La base de datos `restaurante.db` se crea sola la primera vez.

## Estructura

    main.py                      punto de entrada
    data/                        capa de persistencia
        database_manager.py      conexion, commit y rollback con "with"
        repositorio_base.py      clase abstracta con utilidades SQL
        gasto_dao.py, categoria_dao.py, aporte_dao.py
        plato_repository.py, pedido_repository.py
    domain/                      capa de negocio
        gasto.py, categoria.py, plato.py, pedido.py, aporte.py, resumen.py
        validaciones.py
    ui/                          capa de interfaz
        app_view.py              ventana principal y navegacion
        components/              un panel por seccion

## Base de datos

- categorias_gasto (1) -> (N) gastos
- pedidos (1) -> (N) detalles_pedido (N) <- (1) platos
- aportes (tabla independiente para el dinero que se pone en el negocio)

## Uso del monto

Los montos se escriben sin puntos de miles (12500). La coma se toma como decimal.
