from django.urls import path

from . import views

urlpatterns = [
    # Inicio Sesion
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.logout, name="logout"),
    
]
