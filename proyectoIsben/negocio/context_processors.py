from .models import Usuario


def usuario_actual(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return {"usuario_actual": None}
    try:
        return {"usuario_actual": Usuario.objects.get(id=usuario_id)}
    except Usuario.DoesNotExist:
        return {"usuario_actual": None}
