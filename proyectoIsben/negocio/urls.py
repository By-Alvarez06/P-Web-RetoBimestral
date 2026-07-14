from django.urls import path

from . import views

urlpatterns = [
    # Inicio Sesion
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.logout, name="logout"),

    # Vendedores
    path("inicio/", views.dashboard_vendedor, name="dashboard_vendedor"),
    path("crear/pedido/", views.crear_pedido, name="crear_pedido"),
    path("crear/tienda/", views.crear_tienda, name="crear_tienda"),
    path("listar/tiendas/", views.listar_tiendas, name="listar_tiendas"),
    path("editar/tienda/<int:id>", views.editar_tienda, name="editar_tienda"),
    path("editar/pedido/<int:id>", views.editar_pedido, name="editar_pedido"),
    path("ver/pedido/<int:id>/", views.ver_pedido, name="ver_pedido"),
    path("eliminar/pedido/<int:id>/", views.eliminar_pedido, name="eliminar_pedido"),
    path("cambiar/estado/pedido/<int:id>/", views.cambiar_estado, name="cambiar_estado"),
    path("cancelar/pedido/<int:id>/", views.cancelar_pedido, name="cancelar_pedido"),
    path("ver/tienda/<int:id>/", views.ver_tienda, name="ver_tienda"),
    path("eliminar/tienda/<int:id>/", views.eliminar_tienda, name="eliminar_tienda"),
    path("listar/comisiones", views.listar_comisiones, name="listar_comisiones"),
    path("listar/puntos/", views.listar_puntos, name="listar_puntos"),


    # Comercializadora
    path("inicio/comercio/", views.dashboard_comercio, name="dashboard_comercio"),
    path("listar/productos/", views.listar_productos, name="listar_productos"),
    path("crear/producto/", views.crear_producto, name="crear_producto"),
    path("ver/producto/<int:id>/", views.ver_producto, name="ver_producto"),
    path("editar/producto/<int:id>/", views.editar_producto, name="editar_producto"),
    path("eliminar/producto/<int:id>/", views.eliminar_producto, name="eliminar_producto"),
    path("listar/inventario", views.listar_inventario, name="listar_inventario"),
    path("ver/inventario/<int:id>/", views.ver_inventario, name="ver_inventario"),
    path("editar/inventario/<int:id>/", views.editar_inventario, name="editar_inventario"),
    path("listar/liquidacion/", views.listar_liquidacion, name="listar_liquidacion"),
    path("ver/liquidacion/<int:id>/", views.ver_liquidacion, name="ver_liquidacion"),
    path("listar/vendedores/", views.listar_vendedores, name="listar_vendedores"),
    path("ver/vendedor/<int:id>/", views.ver_vendedor, name="ver_vendedor"),
    path("listar/campanas/", views.listar_campanas, name="listar_campanas"),
    path("crear/campana/", views.crear_campana, name="crear_campana"),
    path("ver/campana/<int:id>/", views.ver_campana, name="ver_campana"),
    path("editar/campana/<int:id>/", views.editar_campana, name="editar_campana"),
    path("eliminar/campana/<int:id>/", views.eliminar_campana, name="eliminar_campana"),

]
