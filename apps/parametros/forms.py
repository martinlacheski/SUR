from django.forms import ModelForm, TextInput, Select, EmailInput, PasswordInput

from apps.parametros.models import TiposIVA, CondicionesIVA, CondicionesPago, TiposComprobantes, Marcas, Modelos, \
    Prioridades, Estados, TiposPercepciones, MediosPago, Empresa, EstadoParametros


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
            'iva': TextInput(attrs={
                'class': 'form-control',
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


class TiposPercepcionesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = TiposPercepciones
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'percepcion': TextInput(attrs={
                'class': 'form-control',
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


class MediosPagoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = MediosPago
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
        except Exception as e:
            data['error'] = str(e)
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
                # Obtenemos la INSTANCIA AL GUARDAR PARA OBTENER EL OBJETO Y PASAR AL SELECT2
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ModelosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marca'].widget.attrs['autofocus'] = True

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
                # Obtenemos la INSTANCIA AL GUARDAR PARA OBTENER EL OBJETO Y PASAR AL SELECT2
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EstadosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Estados
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'orden': TextInput(attrs={
                'class': 'form-control',
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


class EstadoParametrosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estadoInicial'].widget.attrs['autofocus'] = True

    class Meta:
        model = EstadoParametros
        fields = '__all__'
        widgets = {
            'estadoInicial': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'estadoPlanificado': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'estadoEspecial': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'estadoFinalizado': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'estadoEntregado': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'estadoCancelado': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
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


class PrioridadesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Prioridades
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'plazoPrioridad': TextInput(attrs={
                'class': 'form-control',
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


class EmpresaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['razonSocial'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'razonSocial': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una Razón Social',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'condicionIVA': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'cuit': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'INGRESE UN CUIT',
                }
            ),
            'localidad': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'INGRESE UNA DIRECCIÓN',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'telefono': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'INGRESE UN NÚMERO DE TELÉFONO',
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un correo electrónico válido',
                    'style': 'width: 100%'
                }
            ),
            'passwordEmail': PasswordInput(render_value=True,
                                           attrs={
                                               'class': 'form-control',
                                               'placeholder': 'Ingrese la contraseña del Correo',
                                               'style': 'width: 100%'
                                           }
                                           ),
            'botTelegram': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Bot de Telegram',
                    'style': 'width: 100%'
                }
            ),
            'tokenTelegram': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Token de Telegram',
                    'style': 'width: 100%'
                }
            ),
            'facebook': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la cuenta de Facebook',
                    'style': 'width: 100%'
                }
            ),
            'instagram': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la cuenta de Instagram',
                    'style': 'width: 100%'
                }
            ),
            'paginaWeb': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la URL del Sitio Web Empresarial',
                    'style': 'width: 100%'
                }
            ),
            'cbu': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un CBU/CVU',
                    'style': 'width: 100%'
                }
            ),
            'alias': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un Alias',
                    'style': 'width: 100%'
                }
            ),
            'nroCuenta': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un Número de Cuenta',
                    'style': 'width: 100%'
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
