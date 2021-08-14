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

    def save(self):
        data = {}
        form = super()
        try:
            form.save()
        except Exception as e:
            data['error'] = str(e)
        return data

    """ Chequea si el pais ya existe y avisa al front-end.
        Si el pais que se ingresa estaba de baja, lo da de alta """
    def checkAndSave (self, post, url_redirect):
        data = {}
        form = PaisesForm(post)
        if form.is_valid():
            # Si existe el pais que se quiere guardar y está activo, error.
            try:
                pais = Paises.objects.get(nombre=form.cleaned_data['nombre'].upper(), estado=True)
                data['check'] = True
            except Exception as e:
                # Si existe pais pero está inactivo, dar de alta.
                try:
                    pais = Paises.objects.get(nombre=form.cleaned_data['nombre'].upper())
                    Paises.objects.filter(pk=pais.id).update(estado=True)
                    data['check'] = False
                    data['redirect'] = url_redirect
                # Si no existe pais en lo absoluto, registrar
                except Exception as e:
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()
        else:
            data['error'] = "Formulario no válido"
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

    def checkAndSave (self, post, url_redirect):
        data = {}
        form = ProvinciasForm(post)
        if (form.is_valid()):
            # Si existe provincia que se quiere guardar y la misma está activa, error.
            try:
                provincia = Provincias.objects.get(nombre=form.cleaned_data['nombre'].upper(),
                                                   pais=form.cleaned_data['pais'], estado=True)
                data['check'] = True
            # Si existe provincia pero está inactiva, dar de alta.
            except Exception as e:
                try:
                    provincia = Provincias.objects.get(nombre=form.cleaned_data['nombre'].upper(),
                                                       pais=form.cleaned_data['pais'])
                    Provincias.objects.filter(pk=provincia.id).update(estado=True)
                    data['check'] = False
                    data['redirect'] = url_redirect
                except Exception as e:
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()
        else:
            data['error'] = "Formulario no válido"
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
