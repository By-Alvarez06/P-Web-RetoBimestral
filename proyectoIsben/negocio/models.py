from django.db import models
# Create your models here.

class Usuario(models.Model):
    ROL_CHOICES = (
        ('VENDEDOR', 'Vendedor'),
        ('COMERCIALIZADORA', 'Comercializadora'),
    )
    
    ruc = models.CharField(max_length=13, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    estado_cuenta = models.BooleanField(default=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return "%s %s - Rol: %s (%s)" % (
            self.nombres, 
            self.apellidos, 
            self.rol, self.ruc
            )

class Vendedor(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name="perfil_vendedor"
        )
    zona_asignada = models.CharField(max_length=100)
    vehiculo_placa = models.CharField(max_length=10)
    puntos_acumulados = models.IntegerField(default=0)
    presupuesto_ventas = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
        )

    def __str__(self):
        return "Vendedor: %s %s - Zona: %s" % (
            self.usuario.nombres,
            self.usuario.apellidos,
            self.zona_asignada
            )

    def nombre_completo(self):
        return "%s %s" % (self.usuario.nombres, self.usuario.apellidos)
    
    def nombre_completo(self):
        return self.usuario.nombres + " " + self.usuario.apellidos
    
    def ruc(self):
        return self.usuario.ruc


class Comercializadora(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name="perfil_comercializadora"
        )
    razon_social = models.CharField(max_length=150)
    nombre_empresa = models.CharField(max_length=150)
    direccion_matriz = models.TextField()
    suscripcion_activa = models.BooleanField(default=True)

    def __str__(self):
        return "Comercializadora: %s - Activa: %s" % (
            self.nombre_empresa, 
            self.suscripcion_activa
            )


class Tienda(models.Model):
    nombre = models.CharField(max_length=100)
    propietario = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    latitud = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        default=-3.986659
        )
    longitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=-79.199088
        )

    def __str__(self):
        return "Tienda: %s - Propietario: %s" % (self.nombre, self.propietario)


class Producto(models.Model):
    comercializadora = models.ForeignKey(
        Comercializadora, 
        on_delete=models.CASCADE, 
        related_name="productos"
        )
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=50)
    precio_mayorista = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "[%s] %s - $%.2f (%s)" % (
            self.sku, self.nombre, 
            self.precio_mayorista, 
            self.comercializadora.nombre_empresa
            )


class Inventario(models.Model):
    producto = models.OneToOneField(
        Producto, 
        on_delete=models.CASCADE, 
        related_name="inventario"
        )
    almacen_origen = models.CharField(max_length=100)
    cantidad_disp = models.PositiveIntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1) # Para Optimistic Locking

    def __str__(self):
        return "Stock: %d uds - %s (Bodega: %s)" % (
            self.cantidad_disp, 
            self.producto.nombre, 
            self.almacen_origen
            )


class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    vendedor = models.ForeignKey(
        Vendedor, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="pedidos_registrados"
        )
    tienda = models.ForeignKey(
        Tienda, 
        on_delete=models.CASCADE, 
        related_name="pedidos_recibidos"
        )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='PENDIENTE'
        )
    monto_total_tienda = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
        )

    def __str__(self):
        return "Pedido #%d - %s - Total: $%.2f - Tienda: %s" % \
        (self.id, self.estado, self.monto_total_tienda, self.tienda.nombre)
    
    def obtener_tienda(self):
        return self.tienda.nombre    


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name="detalles"
        )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.PROTECT, 
        related_name="detalles_vendidos"
        )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "Detalle: %d x %s - Subtotal: $%.2f (Pedido #%d)" % (
            self.cantidad, 
            self.producto.nombre, 
            self.subtotal, 
            self.pedido.id
            )

class LiquidacionComercializadora(models.Model):
    ESTADO_PAGO_CHOICES = (
        ('PENDIENTE_PAGO', 'Pendiente de Pago'),
        ('PAGADO_COMERCIALIZADORA', 'Pagado a Comercializadora'),
    )
    
    pedido = models.OneToOneField(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name="liquidacion"
        )
    monto_comision = models.DecimalField(max_digits=10, decimal_places=2)
    monto_cobrar = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_liquidacion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(
        max_length=30, 
        choices=ESTADO_PAGO_CHOICES, 
        default='PENDIENTE_PAGO'
        )

    def __str__(self):
        return "Liquidación Pedido #%d - Comisión: $%.2f - A cobrar: $%.2f" % (
            self.pedido.id, 
            self.monto_comision, 
            self.monto_cobrar
            )
    
    def vendedor(self):
        vendedor = self.pedido.vendedor
        if vendedor is None:
            return "Vendedor eliminado"
        return vendedor.usuario.nombres + " " + vendedor.usuario.apellidos

class TransaccionPuntos(models.Model):
    TIPO_CHOICES = (
        ('INGRESO', 'Venta (Ingreso)'),
        ('EGRESO', 'Canje (Egreso)'),
    )
    
    vendedor = models.ForeignKey(
        Vendedor, 
        on_delete=models.CASCADE, 
        related_name="transacciones_puntos"
        )
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="puntos_generados"
        )
    tipo_transaccion = models.CharField(max_length=15, choices=TIPO_CHOICES)
    puntos_ganados = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s: %d pts - Vendedor: %s" % (
            self.tipo_transaccion, 
            self.puntos_ganados, 
            self.vendedor.usuario.nombres
            )

class CampanaRecompensa(models.Model):
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE, 
        related_name="campanas"
        )
    nombre_campana = models.CharField(max_length=100)
    factor_puntos = models.PositiveIntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return "Campaña: %s - Producto: %s - (+%d pts)" % (
            self.nombre_campana, 
            self.producto.nombre, 
            self.factor_puntos
            )