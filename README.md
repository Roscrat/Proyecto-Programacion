# La Buena Mesa - Sistema de gestion para un restaurante

Aplicacion de escritorio hecha con Python, Flet y SQLite. Permite tomar pedidos por mesa,
personalizar el almuerzo, cobrar, y llevar el control de gastos y de la plata disponible.

## Como ejecutarlo

    pip install -r requirements.txt
    python main.py

La base de datos `la_buena_mesa.db` se crea sola la primera vez, con mesas, menu y opciones de ejemplo.

## Acceso

La aplicacion no tiene login ni roles: al abrirla se entra directo y todas las secciones
estan disponibles: Inicio (punto de venta), Menu (productos y precios), Pedidos (historial),
Mesas (comanda y cobro), Finanzas (resumen del dinero, aportes y gastos) y Configuracion
(mesas y opciones del almuerzo).

## Estructura

    main.py                      punto de entrada
    data/                        capa de persistencia (SQL)
    domain/                      capa de negocio (clases y validaciones)
    ui/                          capa de interfaz Flet
        app_view.py              barra lateral y navegacion
        contexto.py              objeto compartido por las pantallas
        tema.py                  colores y botones
        components/              una pantalla o ventana por archivo

Hay una guia para estudiar el codigo en `GUIA_DE_ESTUDIO.md`.
