from django.forms import ModelForm, TextInput, Select

from apps.geografico.models import Paises, Provincias, Localidades


class PaisesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Paises
        fields = ['nombre']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProvinciasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Seteamos para que el Select contenga unicamente los registros activos
        self.fields['pais'].queryset = Paises.objects.filter(estado=True)
        self.fields['pais'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provincias
        fields = ['pais', 'nombre']
        widgets = {
            'pais': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class LocalidadesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Seteamos para que el Select contenga unicamente los registros activos
        self.fields['pais'].queryset = Paises.objects.filter(estado=True)
        self.fields['provincia'].queryset = Provincias.objects.filter(estado=True)
        self.fields['pais'].widget.attrs['autofocus'] = True

    class Meta:
        model = Localidades
        fields = ['pais', 'provincia', 'nombre', 'codigo_postal']
        widgets = {
            'pais': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'provincia': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'nombre': TextInput(attrs={
                'placeholder': 'Ingrese un nombre',
                # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                'style': 'text-transform: uppercase'
            }),
            'codigo_postal': TextInput(attrs={
                'placeholder': 'Ingrese un código postal',
                # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                'style': 'text-transform: uppercase'
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
