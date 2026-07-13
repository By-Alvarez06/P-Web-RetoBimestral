from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render

from .decorators import rol_requerido
from .forms import LoginForm, RegistroForm, PedidoForm, TiendaForm
from .models import Comercializadora, Vendedor, Pedido, Tienda


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
    data = {'form':form}

    return render(request, "registro.html", data)


def login(request):
    if request.session.get("usuario_id"):
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.usuario
            request.session["usuario_id"] = usuario.id
            messages.success(request, f"Bienvenido, {usuario.nombres}")

            if usuario.rol == "VENDEDOR":
                return redirect("dashboard_vendedor")
    else:
        form = LoginForm()
    data = {'form': form}

    return render(request, "login.html", data)


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

@rol_requerido("VENDEDOR")
def crear_tienda(request):
    if request.method == "POST":
        form = TiendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_vendedor")
    else:
        form = TiendaForm()
    data = {'form': form}
    return render(request, "vendedor/crear_tienda.html", data)

@rol_requerido("VENDEDOR")
def listar_tiendas(request):
    tiendas = Tienda.objects.all()
    data = {'tiendas': tiendas}
    return render(request, "vendedor/listar_tiendas.html", data)

@rol_requerido("VENDEDOR")
def editar_tienda(request, id):
    tienda = Tienda.objects.get(pk=id)
    if request.method == "POST":
        form = TiendaForm(request.POST, instance=tienda)
        if form.is_valid():
            form.save()
            messages.success(request, "Tienda Actualizada")
            return redirect("listar_tiendas")
    else:
        form = TiendaForm(instance=tienda)
    data = {
        'tienda': tienda,
        'form': form
        }
    return render(request, "vendedor/editar_tienda.html", data)    

@rol_requerido("VENDEDOR")
def editar_pedido(request, id):
    pedido = Pedido.objects.get(pk=id)
    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido actualizado")
            return redirect("dashboard_vendedor")
    else:
        form = PedidoForm(instance = pedido)
    data = {
        'pedido': pedido,
        'form': form
    }    
    return render(request, "vendedor/editar_pedido.html", data)


@rol_requerido("VENDEDOR")
def ver_pedido(request, id):
    pedido = Pedido.objects.get(pk=id)
    data = {'pedido': pedido}
    return render(request, "vendedor/ver_pedido.html", data)

@rol_requerido("VENDEDOR")
def eliminar_pedido(request, id):
    pedido = Pedido.objects.get(pk=id)
    if request.method == "POST":
        pedido.delete()
        messages.success(request, "Pedido eliminado")
        return redirect("dashboard_vendedor")
    data = {'pedido': pedido}
    return render(request, "vendedor/eliminar_pedido.html", data)

@rol_requerido("VENDEDOR")
def ver_tienda(request, id):
    tienda = Tienda.objects.get(pk=id)
    data = {
        'tienda': tienda
    }
    return render(request, "vendedor/ver_tienda.html", data)

@rol_requerido("VENDEDOR")
def eliminar_tienda(request, id):
    tienda = Tienda.objects.get(pk=id)
    if request.method=="POST":
        tienda.delete()
        messages.success(request, "Tienda eliminada")
        return redirect("listar_tiendas")
    data = {'tienda': tienda}
    return render(request, "vendedor/eliminar_tienda.html", data)