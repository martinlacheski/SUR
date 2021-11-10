from django.forms import ModelForm, TextInput, Select

from apps.geografico.models import Paises, Provincias, Localidades


class PaisesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Paises
        fields = '__all__'
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
        self.fields['pais'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provincias
        fields = '__all__'
        widgets = {
            'pais': Select(attrs={
                'class': 'form-select form-control select2',
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
        self.fields['pais'].widget.attrs['autofocus'] = True

    class Meta:
        model = Localidades
        fields = '__all__'
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

    # def checkAndSave(self, form, url_redirect, action):
    #     data = {}
    #     if form.is_valid():
    #         # Si existe el objeto que se quiere guardar/editar y está activo, error.
    #         try:
    #             localidad = Localidades.objects.get(nombre=form.cleaned_data['nombre'].upper(),
    #                                                 pais=form.cleaned_data['pais'],
    #                                                 provincia=form.cleaned_data['provincia'])
    #             data['check'] = True
    #         except Exception as e:
    #             if action == 'add':
    #                 data['check'] = 'Registrar'
    #                 data['redirect'] = url_redirect
    #                 form.save()
    #
    #             # action 'edit'
    #             elif action == 'edit':
    #                 data['check'] = 'Registrar'
    #                 data['redirect'] = url_redirect
    #                 form.save()
    #
    #     else:
    #         data['error'] = "Formulario no válido"
    #     return data
