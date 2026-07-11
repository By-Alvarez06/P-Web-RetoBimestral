from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render

from .decorators import rol_requerido
from .forms import LoginForm, RegistroForm, PedidoForm
from .models import Comercializadora, Usuario, Vendedor, Pedido


def home(request):
    return render(request, "home.html")


def registro(request):
    if request.session.get("usuario_id"):
        return redirect("home")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usuario = form.save(commit=False)
            usuario.password = make_password(data["password"])
            usuario.save()

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
            if usuario.rol == "VENDEDOR":
                request.session["usuario_id"] = usuario.id
                messages.success(request, f"Bienvenido, {usuario.nombres}")
                return redirect("dashboard_vendedor")

    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})


def login(request):
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
            if usuario.rol == "VENDEDOR":
                request.session["usuario_id"] = usuario.id
                return redirect("dashboard_vendedor")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("home")


@rol_requerido("VENDEDOR")
def dashboard_vendedor(request):
    pedidos = Pedido.objects.filter(vendedor=request.usuario.perfil_vendedor)
    data = {
        'pedidos': pedidos
    }
    return render(request, "vendedor/dashboard_vendedor.html", data)

@rol_requerido("VENDEDOR")
def crear_pedido(request):
    vendedor = request.usuario.perfil_vendedor

    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.vendedor = vendedor
            pedido.save()
            return redirect("dashboard_vendedor")
    else:
        form = PedidoForm()
    data = {'form': form}
    return render(request, "vendedor/crear_pedido.html", data)