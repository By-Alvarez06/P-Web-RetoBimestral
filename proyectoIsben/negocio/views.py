from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render, get_object_or_404

from .decorators import rol_requerido
from .forms import LoginForm, RegistroForm, PedidoForm, TiendaForm, \
                    ProductoForm, InventarioForm
from .models import Comercializadora, Vendedor, Pedido, Tienda, \
                    LiquidacionComercializadora, Producto, Inventario


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
            request.session["usuario_id"] = usuario.id
            messages.success(request, f"Bienvenido, {usuario.nombres}")
            if usuario.rol == "VENDEDOR": 
                return redirect("dashboard_vendedor")
            elif usuario.rol == "COMERCIALIZADORA":
                return redirect("dashboard_comercio")
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
            elif usuario.rol == "COMERCIALIZADORA":
                return redirect("dashboard_comercio")
    else:
        form = LoginForm()
    data = {'form': form}

    return render(request, "login.html", data)


def logout(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("home")


# VENDEDORES

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
            return redirect("listar_tiendas")
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

@rol_requerido("VENDEDOR")
def listar_comisiones(request):
    vendedor = request.usuario.perfil_vendedor
    comisiones = LiquidacionComercializadora.objects.filter(pedido__vendedor=vendedor)
    data = {'comisiones': comisiones}
    return render(request, "vendedor/listar_comisiones.html", data)

# COMERCIALIZADORA

@rol_requerido("COMERCIALIZADORA")
def dashboard_comercio(request):
    comercializadora = request.usuario.perfil_comercializadora
    productos_totales = Producto.objects.filter(comercializadora=comercializadora).count()
    data = {
        'productos_totales': productos_totales
    }
    return render(request, "comercio/dashboard_comercio.html", data)


@rol_requerido("COMERCIALIZADORA")
def listar_productos(request):
    comercializadora = request.usuario.perfil_comercializadora
    # Traemos los productos junto con su inventario usando select_related para optimizar la consulta
    productos = Producto.objects.filter(comercializadora=comercializadora).select_related('inventario')
    data = {'productos': productos}
    return render(request, "comercio/listar_productos.html", data)

@rol_requerido("COMERCIALIZADORA")
def ver_producto(request, id):
    producto = Producto.objects.get(pk=id)
    data = {'producto': producto}
    return render(request, "comercio/ver_producto.html", data)


@rol_requerido("COMERCIALIZADORA")
def crear_producto(request):
    comercializadora = request.usuario.perfil_comercializadora

    if request.method == "POST":
        form_producto = ProductoForm(request.POST)
        form_inventario = InventarioForm(request.POST)
        
        if form_producto.is_valid() and form_inventario.is_valid():
            # Guardamos el producto asignándole la comercializadora actual
            producto = form_producto.save(commit=False)
            producto.comercializadora = comercializadora
            producto.save()
            
            # Guardamos el inventario vinculándolo al producto recién creado
            inventario = form_inventario.save(commit=False)
            inventario.producto = producto
            inventario.save()
            
            messages.success(request, "Producto e inventario creados con éxito.")
            return redirect("listar_productos")
    else:
        form_producto = ProductoForm()
        form_inventario = InventarioForm()
        
    data = {
        'form_producto': form_producto,
        'form_inventario': form_inventario
    }
    return render(request, "comercio/crear_producto.html", data)


@rol_requerido("COMERCIALIZADORA")
def editar_producto(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    # Nos aseguramos de que el producto pertenezca a la comercializadora logueada
    producto = Producto.objects.get(pk=id, comercializadora=comercializadora)
    
    # Tratamos de obtener el inventario, si no existe (por error de base de datos) lo dejamos en None
    inventario = getattr(producto, 'inventario', None)

    if request.method == "POST":
        form_producto = ProductoForm(request.POST, instance=producto)
        form_inventario = InventarioForm(request.POST, instance=inventario)
        
        if form_producto.is_valid() and form_inventario.is_valid():
            form_producto.save()
            
            if inventario is None:
                nuevo_inventario = form_inventario.save(commit=False)
                nuevo_inventario.producto = producto
                nuevo_inventario.save()
            else:
                form_inventario.save()
                
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("listar_productos")
    else:
        form_producto = ProductoForm(instance=producto)
        form_inventario = InventarioForm(instance=inventario)
        
    data = {
        'producto': producto,
        'form_producto': form_producto,
        'form_inventario': form_inventario
    }
    return render(request, "comercio/editar_producto.html", data)


@rol_requerido("COMERCIALIZADORA")
def eliminar_producto(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    producto = Producto.objects.get(pk=id, comercializadora=comercializadora)
    
    if request.method == "POST":
        # Al tener on_delete=models.CASCADE en el inventario, se borrará automáticamente
        producto.delete()
        messages.success(request, "Producto eliminado exitosamente.")
        return redirect("listar_productos")
        
    data = {'producto': producto}
    return render(request, "comercio/eliminar_producto.html", data)

@rol_requerido("COMERCIALIZADORA")
def listar_inventario(request):
    comercializadora = request.usuario.perfil_comercializadora
    # Filtramos los inventarios cruzando la relación hacia el producto de esta comercializadora
    inventarios = Inventario.objects.filter(
        producto__comercializadora=comercializadora
    ).select_related('producto')
    
    data = {'inventarios': inventarios}
    return render(request, "comercio/listar_inventario.html", data)


@rol_requerido("COMERCIALIZADORA")
def ver_inventario(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    inventario = get_object_or_404(
        Inventario, 
        pk=id, 
        producto__comercializadora=comercializadora
    )
    
    data = {'inventario': inventario}
    return render(request, "comercio/ver_inventario.html", data)


@rol_requerido("COMERCIALIZADORA")
def editar_inventario(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    # Validación de seguridad: Asegurar que editen solo SU inventario
    inventario = get_object_or_404(
        Inventario, 
        pk=id, 
        producto__comercializadora=comercializadora
    )

    if request.method == "POST":
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            form.save()
            messages.success(request, f"Stock actualizado para: {inventario.producto.nombre}")
            return redirect("listar_inventario")
    else:
        form = InventarioForm(instance=inventario)

    data = {
        'inventario': inventario,
        'form': form
    }
    return render(request, "comercio/editar_inventario.html", data)