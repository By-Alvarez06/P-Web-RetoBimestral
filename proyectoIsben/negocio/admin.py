from django.contrib import admin
from .models import Usuario, Vendedor, Comercializadora, Tienda, Producto, Inventario, \
Pedido, DetallePedido, TransaccionPuntos, LiquidacionComercializadora, CampanaRecompensa

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Vendedor)
admin.site.register(Comercializadora)
admin.site.register(Tienda)
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(LiquidacionComercializadora)
admin.site.register(TransaccionPuntos)
admin.site.register(CampanaRecompensa)