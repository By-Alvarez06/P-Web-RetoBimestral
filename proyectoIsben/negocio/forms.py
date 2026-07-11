from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import Usuario, Pedido, Tienda

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "tucorreo@ejemplo.com", "autofocus": True}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••"}),
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")

        if email and password:
            usuario = Usuario.objects.filter(email=email).first()
            if usuario is None or not check_password(password, usuario.password):
                raise forms.ValidationError("Correo o contraseña incorrectos.")
            if not usuario.estado_cuenta:
                raise forms.ValidationError("Tu cuenta está desactivada. Contacta al administrador.")
            self.usuario = usuario

        return cleaned


class RegistroForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    zona_asignada = forms.CharField(label="Zona asignada", max_length=100, required=False)
    vehiculo_placa = forms.CharField(label="Placa del vehículo", max_length=10, required=False)

    razon_social = forms.CharField(label="Razón social", max_length=150, required=False)
    nombre_empresa = forms.CharField(label="Nombre de la empresa", max_length=150, required=False)
    direccion_matriz = forms.CharField(label="Dirección de la matriz", widget=forms.Textarea, required=False)

    class Meta:
        model = Usuario
        fields = ["rol", "ruc", "nombres", "apellidos", "email"]
        widgets = {"rol": forms.RadioSelect}
        labels = {
            "rol": "Tipo de cuenta",
            "ruc": "RUC",
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "email": "Correo electrónico",
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")
        return email

    def clean_ruc(self):
        ruc = self.cleaned_data["ruc"]
        if Usuario.objects.filter(ruc=ruc).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este RUC.")
        return ruc

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        password2 = cleaned.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        rol = cleaned.get("rol")
        if rol == "VENDEDOR":
            for campo in ("zona_asignada", "vehiculo_placa"):
                if not cleaned.get(campo):
                    self.add_error(campo, "Este campo es obligatorio para vendedores.")
        elif rol == "COMERCIALIZADORA":
            for campo in ("razon_social", "nombre_empresa", "direccion_matriz"):
                if not cleaned.get(campo):
                    self.add_error(campo, "Este campo es obligatorio para comercializadoras.")
        return cleaned


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['tienda', 'monto_total_tienda']

class TiendaForm(forms.ModelForm):
    class Meta:
        model= Tienda
        fields = ['nombre', 'propietario', 'direccion', 'telefono', 'latitud', 'longitud']

    def clean_propietario(self):
        valor = self.cleaned_data.get("propietario")
        num_palabras = len(valor.split())
        if num_palabras < 2:
            raise ValidationError("El nombre del propietario debe ser almenos nombre y apellido")    
        return valor 

    def clean_latitud(self):
        latitud = self.cleaned_data.get("latitud")
        if latitud < -90 or latitud > 90:
            raise forms.ValidationError(
                "La latitud debe estar entre -90 y 90."
            )
        return latitud

    def clean_longitud(self):
        longitud = self.cleaned_data.get("longitud")
        if longitud < -180 or longitud > 180:
            raise forms.ValidationError(
                "La longitud debe estar entre -180 y 180."
            )
        return longitud   