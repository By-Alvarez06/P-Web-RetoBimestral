from django.contrib import admin
from .models import Usuario, Vendedor, Comercializadora, Tienda, Producto

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Vendedor)
admin.site.register(Comercializadora)
admin.site.register(Tienda)
admin.site.register(Producto)