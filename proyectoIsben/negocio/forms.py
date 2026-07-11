from django import forms

from .models import Usuario, Pedido


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "tucorreo@ejemplo.com", "autofocus": True}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••"}),
    )


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