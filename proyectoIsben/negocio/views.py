from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404

from .decorators import login_requerido, rol_requerido
from .forms import LoginForm, RegistroForm, PedidoForm, \
                    ProductoForm, InventarioForm, DetalleFormSet, CampanaRecompensaForm
from .models import StockInsuficienteError, Comercializadora, Vendedor, Pedido, Tienda, \
                    LiquidacionComercializadora, Producto, Inventario, InventarioTienda, \
                    CampanaRecompensa, TransaccionPuntos

def _cantidades_por_producto(formset):
    """Suma las cantidades solicitadas por producto en un formset de detalles válido."""
    cantidades = {}
    for detalle_form in formset:
        cleaned = detalle_form.cleaned_data
        if not cleaned or cleaned.get("DELETE"):
            continue
        producto = cleaned.get("producto")
        cantidad = cleaned.get("cantidad")
        if producto and cantidad:
            cantidades[producto.id] = cantidades.get(producto.id, 0) + cantidad
    return cantidades


def _pedido_propio(usuario, id):
    """Obtiene un pedido asegurando que pertenezca al vendedor o tienda que hace la solicitud."""
    if usuario.rol == "TIENDA":
        return get_object_or_404(Pedido, pk=id, tienda=usuario.perfil_tienda)
    return get_object_or_404(Pedido, pk=id, vendedor=usuario.perfil_vendedor)


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
            elif data["rol"] == "COMERCIALIZADORA":
                Comercializadora.objects.create(
                    usuario=usuario,
                    razon_social=data["razon_social"],
                    nombre_empresa=data["nombre_empresa"],
                    direccion_matriz=data["direccion_matriz"],
                )
            else:
                Tienda.objects.create(
                    usuario = usuario,
                    nombre = data["nombre"],
                    direccion = data["direccion"],
                    latitud = data["latitud"],
                    longitud = data["longitud"]
                )    
            request.session["usuario_id"] = usuario.id
            messages.success(request, f"Bienvenido, {usuario.nombres}")
            if usuario.rol == "VENDEDOR": 
                return redirect("dashboard_vendedor")
            elif usuario.rol == "COMERCIALIZADORA":
                return redirect("dashboard_comercio")
            elif usuario.rol == "TIENDA":
                return redirect("dashboard_tienda")
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
            elif usuario.rol == "TIENDA":
                return redirect("dashboard_tienda")
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

# ==========================================
# GESTIÓN DE PEDIDOS DEL VENDEDOR
# ==========================================

@rol_requerido("VENDEDOR", "TIENDA")
def crear_pedido(request):
    es_tienda = request.usuario.rol == "TIENDA"
    form = None

    if request.method == "POST":
        formset = DetalleFormSet(request.POST, prefix="detalles")
        if not es_tienda:
            form = PedidoForm(request.POST)

        if (form is None or form.is_valid()) and formset.is_valid():
            cantidades = _cantidades_por_producto(formset)

            if not cantidades:
                messages.error(request, "Debe agregar al menos un producto al pedido.")
            else:
                try:
                    with transaction.atomic():
                        if es_tienda:
                            pedido = Pedido(tienda=request.usuario.perfil_tienda)
                        else:
                            pedido = form.save(commit=False)
                            pedido.vendedor = request.usuario.perfil_vendedor
                        pedido.save()

                        formset.instance = pedido
                        detalles = formset.save(commit=False)
                        total = Decimal("0.00")

                        for detalle in detalles:
                            inventario = Inventario.objects.select_for_update().get(producto=detalle.producto)
                            inventario.ajustar_stock(detalle.cantidad)

                            detalle.pedido = pedido
                            detalle.precio_unitario = detalle.producto.precio_mayorista
                            detalle.subtotal = detalle.precio_unitario * detalle.cantidad
                            detalle.save()
                            total += detalle.subtotal

                        for obj in formset.deleted_objects:
                            obj.delete()

                        pedido.monto_total_tienda = total
                        pedido.save()
                        
                        # Delegación de lógica al modelo
                        pedido.generar_liquidacion()
                        pedido.registrar_puntos()
                        
                except StockInsuficienteError as error:
                    messages.error(request, str(error))
                else:
                    messages.success(request, "Pedido creado con éxito.")
                    return redirect("listar_pedidos_tienda" if es_tienda else "dashboard_vendedor")
    else:
        formset = DetalleFormSet(prefix="detalles")
        if not es_tienda:
            form = PedidoForm()

    data = {'form': form, 'formset': formset}
    plantilla = "tienda/crear_pedido.html" if es_tienda else "vendedor/crear_pedido.html"
    return render(request, plantilla, data)

@rol_requerido("VENDEDOR", "TIENDA")
def editar_pedido(request, id):
    es_tienda = request.usuario.rol == "TIENDA"
    pedido = _pedido_propio(request.usuario, id)
    form = None

    if request.method == "POST":
        formset = DetalleFormSet(request.POST, instance=pedido, prefix="detalles")
        if not es_tienda:
            form = PedidoForm(request.POST, instance=pedido)

        if (form is None or form.is_valid()) and formset.is_valid():
            cantidades_previas = {d.producto_id: d.cantidad for d in pedido.detalles.all()}
            cantidades_nuevas = _cantidades_por_producto(formset)

            if not cantidades_nuevas:
                messages.error(request, "Debe agregar al menos un producto al pedido.")
            else:
                try:
                    with transaction.atomic():
                        productos_ids = set(cantidades_previas) | set(cantidades_nuevas)
                        for producto_id in productos_ids:
                            inventario = Inventario.objects.select_for_update().get(producto_id=producto_id)
                            requerido = cantidades_nuevas.get(producto_id, 0)
                            previa = cantidades_previas.get(producto_id, 0)
                            inventario.ajustar_stock(requerido, cantidad_previa=previa)

                        if form is not None:
                            form.save()
                        detalles = formset.save(commit=False)
                        for detalle in detalles:
                            detalle.pedido = pedido
                            detalle.precio_unitario = detalle.producto.precio_mayorista
                            detalle.subtotal = detalle.precio_unitario * detalle.cantidad
                            detalle.save()
                            
                        for obj in formset.deleted_objects:
                            obj.delete()

                        pedido.monto_total_tienda = sum((d.subtotal for d in pedido.detalles.all()), Decimal("0.00"))
                        pedido.save()

                        # Delegación de lógica al modelo
                        pedido.generar_liquidacion()
                        pedido.registrar_puntos()
                        
                except StockInsuficienteError as error:
                    messages.error(request, str(error))
                else:
                    messages.success(request, "Pedido actualizado")
                    return redirect("listar_pedidos_tienda" if es_tienda else "dashboard_vendedor")
    else:
        formset = DetalleFormSet(instance=pedido, prefix="detalles")
        if not es_tienda:
            form = PedidoForm(instance=pedido)

    data = {'pedido': pedido, 'form': form, 'formset': formset}
    plantilla = "tienda/editar_pedido.html" if es_tienda else "vendedor/editar_pedido.html"
    return render(request, plantilla, data)

@rol_requerido("VENDEDOR", "TIENDA")
def ver_pedido(request, id):
    pedido = _pedido_propio(request.usuario, id)
    data = {'pedido': pedido}
    plantilla = "tienda/ver_pedido.html" if request.usuario.rol == "TIENDA" else "vendedor/ver_pedido.html"
    return render(request, plantilla, data)

@rol_requerido("VENDEDOR", "TIENDA")
def eliminar_pedido(request, id):
    es_tienda = request.usuario.rol == "TIENDA"
    pedido = _pedido_propio(request.usuario, id)
    if request.method == "POST":
        if pedido.estado == "ENTREGADO":
            messages.error(request, "No se puede eliminar un pedido ya entregado.")
            return redirect("ver_pedido", id=pedido.id)

        with transaction.atomic():
            if pedido.estado != "CANCELADO":
                pedido.restaurar_inventario()
                pedido.revertir_puntos()
            pedido.delete()
        messages.success(request, "Pedido eliminado")
        return redirect("listar_pedidos_tienda" if es_tienda else "dashboard_vendedor")

    data = {'pedido': pedido}
    plantilla = "tienda/eliminar_pedido.html" if es_tienda else "vendedor/eliminar_pedido.html"
    return render(request, plantilla, data)

@rol_requerido("VENDEDOR", "TIENDA")
def cancelar_pedido(request, id):
    pedido = _pedido_propio(request.usuario, id)

    if request.method == "POST":
        if pedido.estado in ("ENTREGADO", "CANCELADO"):
            messages.error(request, "Este pedido ya no se puede cancelar.")
        else:
            with transaction.atomic():
                pedido.restaurar_inventario()
                pedido.revertir_puntos()
                pedido.estado = "CANCELADO"
                pedido.save()
            messages.success(request, "Pedido cancelado")

    return redirect("ver_pedido", id=pedido.id)

@rol_requerido("VENDEDOR")
def listar_comisiones(request):
    vendedor = request.usuario.perfil_vendedor
    comisiones = LiquidacionComercializadora.objects.filter(pedido__vendedor=vendedor)
    data = {'comisiones': comisiones}
    return render(request, "vendedor/listar_comisiones.html", data)

@rol_requerido("VENDEDOR")
def listar_puntos(request):
    vendedor = request.usuario.perfil_vendedor
    transacciones = TransaccionPuntos.objects.filter(vendedor=vendedor).select_related('pedido').order_by('-fecha')
    data = {'vendedor': vendedor, 'transacciones': transacciones}
    return render(request, "vendedor/listar_puntos.html", data)

SECUENCIA_ESTADOS = ['PENDIENTE', 'CONFIRMADO', 'ENTREGADO']


@rol_requerido("VENDEDOR", "TIENDA")
def cambiar_estado(request, id):
    pedido = _pedido_propio(request.usuario, id)

    if request.method == "POST":
        if pedido.estado not in SECUENCIA_ESTADOS:
            messages.error(request, "No se puede avanzar el estado de un pedido cancelado.")
        else:
            indice = SECUENCIA_ESTADOS.index(pedido.estado)
            if indice == len(SECUENCIA_ESTADOS) - 1:
                messages.error(request, "El pedido ya está en su estado final.")
            else:
                pedido.estado = SECUENCIA_ESTADOS[indice + 1]
                pedido.save()
                if pedido.estado == "ENTREGADO":
                    pedido.actualizar_inventario_tienda()
                messages.success(request, f"Pedido actualizado a {pedido.get_estado_display()}")

    return redirect("ver_pedido", id=pedido.id)


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

@rol_requerido("COMERCIALIZADORA")
def listar_liquidacion(request):
    comercializadora = request.usuario.perfil_comercializadora
    liquidaciones = LiquidacionComercializadora.objects.filter(
        pedido__detalles__producto__comercializadora=comercializadora
    ).distinct().select_related("pedido__vendedor__usuario")
    data = {'liquidaciones': liquidaciones}
    return render(request, "comercio/listar_liquidacion.html", data)

@rol_requerido("COMERCIALIZADORA")
def ver_liquidacion(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    liquidacion = get_object_or_404(
        LiquidacionComercializadora.objects.distinct(),
        pk=id,
        pedido__detalles__producto__comercializadora=comercializadora,
    )
    data = {'liquidacion': liquidacion}
    return render(request, "comercio/ver_liquidacion.html", data)

@rol_requerido("COMERCIALIZADORA")
def listar_vendedores(request):
    comercializadora = request.usuario.perfil_comercializadora
    vendedores = Vendedor.objects.filter(
        pedidos_registrados__detalles__producto__comercializadora=comercializadora
    ).distinct().select_related("usuario")
    data = {'vendedores': vendedores}
    return render(request, "comercio/listar_vendedores.html", data)

@rol_requerido("COMERCIALIZADORA")
def ver_vendedor(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    vendedor = get_object_or_404(
        Vendedor.objects.distinct().select_related("usuario"),
        pk=id,
        pedidos_registrados__detalles__producto__comercializadora=comercializadora,
    )
    liquidaciones = LiquidacionComercializadora.objects.filter(
        pedido__vendedor=vendedor,
        pedido__detalles__producto__comercializadora=comercializadora,
    ).distinct().select_related("pedido")
    data = {'vendedor': vendedor, 'liquidaciones': liquidaciones}
    return render(request, "comercio/ver_vendedor.html", data)

@rol_requerido("COMERCIALIZADORA")
def listar_campanas(request):
    comercializadora = request.usuario.perfil_comercializadora
    campanas = CampanaRecompensa.objects.filter(
        producto__comercializadora=comercializadora
    ).select_related('producto')
    data = {'campanas': campanas}
    return render(request, "comercio/listar_campanas.html", data)

@rol_requerido("COMERCIALIZADORA")
def ver_campana(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    campana = get_object_or_404(
        CampanaRecompensa, pk=id, producto__comercializadora=comercializadora
    )
    data = {'campana': campana}
    return render(request, "comercio/ver_campana.html", data)

@rol_requerido("COMERCIALIZADORA")
def crear_campana(request):
    comercializadora = request.usuario.perfil_comercializadora

    if request.method == "POST":
        form = CampanaRecompensaForm(request.POST, comercializadora=comercializadora)
        if form.is_valid():
            form.save()
            messages.success(request, "Campaña de recompensa creada con éxito.")
            return redirect("listar_campanas")
    else:
        form = CampanaRecompensaForm(comercializadora=comercializadora)

    data = {'form': form}
    return render(request, "comercio/crear_campana.html", data)

@rol_requerido("COMERCIALIZADORA")
def editar_campana(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    campana = get_object_or_404(
        CampanaRecompensa, pk=id, producto__comercializadora=comercializadora
    )

    if request.method == "POST":
        form = CampanaRecompensaForm(request.POST, instance=campana, comercializadora=comercializadora)
        if form.is_valid():
            form.save()
            messages.success(request, "Campaña actualizada correctamente.")
            return redirect("ver_campana", id=campana.id)
    else:
        form = CampanaRecompensaForm(instance=campana, comercializadora=comercializadora)

    data = {'campana': campana, 'form': form}
    return render(request, "comercio/editar_campana.html", data)

@rol_requerido("COMERCIALIZADORA")
def eliminar_campana(request, id):
    comercializadora = request.usuario.perfil_comercializadora
    campana = get_object_or_404(
        CampanaRecompensa, pk=id, producto__comercializadora=comercializadora
    )

    if request.method == "POST":
        campana.delete()
        messages.success(request, "Campaña eliminada exitosamente.")
        return redirect("listar_campanas")

    data = {'campana': campana}
    return render(request, "comercio/eliminar_campana.html", data)

@login_requerido
def listar_tiendas(request):
    tiendas = Tienda.objects.all()
    data = {'tiendas': tiendas}
    plantilla = "comercio/listar_tiendas.html" if request.usuario.rol == "COMERCIALIZADORA" else "vendedor/listar_tiendas.html"
    return render(request, plantilla, data)

@login_requerido
def ver_tienda(request, id):
    tienda = get_object_or_404(Tienda, pk=id)
    data = {'tienda': tienda}
    plantilla = "comercio/ver_tienda.html" if request.usuario.rol == "COMERCIALIZADORA" else "vendedor/ver_tienda.html"
    return render(request, plantilla, data)

@rol_requerido("COMERCIALIZADORA")
def liquidacion_pagada(request, id):
    liquidacion = get_object_or_404(
        LiquidacionComercializadora,
        pk=id
    )
    if request.method == "POST":
        if liquidacion.estado_pago == "PAGADO":
            messages.error(request, "La liquidación ya fue pagada.")
        else:
            liquidacion.estado_pago = "PAGADO"
            liquidacion.save()
            messages.success(request, "Pago registrado correctamente.")

    return redirect("ver_liquidacion", id=id)

# Tienda

@rol_requerido("TIENDA")
def dashboard_tienda(request):
    tienda = request.usuario.perfil_tienda
    inventarios = InventarioTienda.objects.filter(tienda=tienda).select_related('producto')
    data = {'inventarios': inventarios}
    return render(request, "tienda/dashboard_tienda.html", data)

@rol_requerido("TIENDA")
def listar_pedidos_tienda(request):
    tienda = request.usuario.perfil_tienda
    pedidos = Pedido.objects.filter(tienda=tienda).order_by('-fecha')
    data = {'pedidos': pedidos}
    return render(request, "tienda/listar_pedidos.html", data)