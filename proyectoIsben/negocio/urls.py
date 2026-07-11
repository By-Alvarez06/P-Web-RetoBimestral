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
    path("editar/pedido/<int:id>", views.editar_pedido, name="editar_pedido")
]
