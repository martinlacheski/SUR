from django.forms import ModelForm, TextInput, Select

from apps.parametros.models import TiposIVA, CondicionesIVA, CondicionesPago, TiposComprobantes, Marcas, Modelos


class TiposIVAForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = TiposIVA
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


class CondicionesIVAForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = CondicionesIVA
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


class CondicionesPagoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = CondicionesPago
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


class TiposComprobantesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = TiposComprobantes
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
                print(form.errors)
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return data


class MarcasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Marcas
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
                print(form.errors)
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return data


class ModelosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Modelos
        fields = '__all__'
        widgets = {
            'marca': Select(attrs={
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
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
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
                print(form.errors)
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return data
