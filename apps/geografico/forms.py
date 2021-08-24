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
        Si el pais que se ingresa estaba de baja, lo da de alta.
        También controla duplicados al momento de editar """

    def checkAndSave(self, form, url_redirect, action):
        data = {}
        if form.is_valid():
            # Si existe el pais que se quiere guardar/editar y está activo, error.
            try:
                pais = Paises.objects.get(nombre=form.cleaned_data['nombre'].upper())
                data['check'] = True
            except Exception as e:
                if action == 'add':
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()
                # action 'edit'
                elif action == 'edit':
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

    def checkAndSave(self, form, url_redirect, action):
        data = {}
        if form.is_valid():
            # Si existe la provincia que se quiere guardar/editar y está activo, error.
            try:
                provincia = Provincias.objects.get(nombre=form.cleaned_data['nombre'].upper(),
                                                   pais=form.cleaned_data['pais'])
                data['check'] = True
            except Exception as e:
                if action == 'add':
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()
                # action 'edit'
                elif action == 'edit':
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

    def checkAndSave(self, form, url_redirect, action):
        data = {}
        if form.is_valid():
            # Si existe la localidad que se quiere guardar/editar y está activo, error.
            try:
                localidad = Localidades.objects.get(nombre=form.cleaned_data['nombre'].upper(),
                                                    pais=form.cleaned_data['pais'],
                                                    provincia=form.cleaned_data['provincia'])
                data['check'] = True
            except Exception as e:
                if action == 'add':
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()

                # action 'edit'
                elif action == 'edit':
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()

        else:
            data['error'] = "Formulario no válido"
        return data
