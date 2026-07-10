from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistroForm
from .models import Comercializadora, Usuario, Vendedor


def home(request):
    return render(request, "home.html")


def registro_view(request):
    if request.session.get("usuario_id"):
        return redirect("home")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usuario = Usuario.objects.create(
                ruc=data["ruc"],
                nombres=data["nombres"],
                apellidos=data["apellidos"],
                email=data["email"],
                password=make_password(data["password"]),
                rol=data["rol"],
            )
            if data["rol"] == "VENDEDOR":
                Vendedor.objects.create(
                    usuario=usuario,
                    zona_asignada=data["zona_asignada"],
                    vehiculo_placa=data["vehiculo_placa"],
                )
            else:
                Comercializadora.objects.create(
                    usuario=usuario,
                    razon_social=data["razon_social"],
                    nombre_empresa=data["nombre_empresa"],
                    direccion_matriz=data["direccion_matriz"],
                )
            messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
            return redirect("login")
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})


def login_view(request):
    if request.session.get("usuario_id"):
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            usuario = Usuario.objects.filter(email=email).first()

            if usuario is None or not check_password(password, usuario.password):
                form.add_error(None, "Correo o contraseña incorrectos.")
            elif not usuario.estado_cuenta:
                form.add_error(None, "Tu cuenta está desactivada. Contacta al administrador.")
            else:
                request.session["usuario_id"] = usuario.id
                messages.success(request, f"Bienvenido, {usuario.nombres}")
                return redirect("home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("home")
