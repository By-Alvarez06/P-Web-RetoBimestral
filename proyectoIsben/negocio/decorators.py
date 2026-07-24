from django.contrib import messages
from django.shortcuts import redirect

from .models import Usuario


def login_requerido(vista):
    """El usuario debe haber iniciado sesión para entrar a esta vista."""

    def nueva_vista(request, *args, **kwargs):
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return redirect("login")

        usuario = Usuario.objects.filter(id=usuario_id, estado_cuenta=True).first()
        if usuario is None:
            request.session.flush()
            return redirect("login")

        request.usuario = usuario
        return vista(request, *args, **kwargs)

    return nueva_vista


def rol_requerido(*roles_permitidos):
    """Además de tener sesión iniciada, el usuario debe tener alguno de los roles indicados.
    @rol_requerido("VENDEDOR")
    @rol_requerido("VENDEDOR", "TIENDA")
    """

    def decorador(vista):
        def nueva_vista(request, *args, **kwargs):
            usuario_id = request.session.get("usuario_id")
            if not usuario_id:
                return redirect("login")

            usuario = Usuario.objects.filter(id=usuario_id, estado_cuenta=True).first()
            if usuario is None:
                request.session.flush()
                return redirect("login")

            if usuario.rol not in roles_permitidos:
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return redirect("home")

            request.usuario = usuario
            return vista(request, *args, **kwargs)

        return nueva_vista

    return decorador
