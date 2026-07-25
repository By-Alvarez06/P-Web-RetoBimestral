from django.db import migrations

CATEGORIAS = [
    "Bebidas",
    "Lácteos",
    "Snacks",
    "Limpieza",
    "Comida",
    "Enlatados",
    "Panadería",
]


def crear_categorias(apps, schema_editor):
    Categoria = apps.get_model('negocio', 'Categoria')
    for nombre in CATEGORIAS:
        Categoria.objects.get_or_create(nombre=nombre)


def eliminar_categorias(apps, schema_editor):
    Categoria = apps.get_model('negocio', 'Categoria')
    Categoria.objects.filter(nombre__in=CATEGORIAS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('negocio', '0005_rename_sku_producto_codigo'),
    ]

    operations = [
        migrations.RunPython(crear_categorias, eliminar_categorias),
    ]
