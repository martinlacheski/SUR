from django.forms import ModelForm, DateInput, Select, TextInput

from apps.trabajos.models import Trabajos, PlanificacionesSemanales


class TrabajosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Trabajos
        fields = '__all__'
        widgets = {
            'fechaEntrada': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'fechaEntrada',
                    'data-target': '#fechaEntrada',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'fechaSalida': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'fechaSalida',
                    'data-target': '#fechaSalida',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'cliente': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'modelo': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'usuarioAsignado': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'iva': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'percepcion': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'prioridad': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'estadoTrabajo': Select(
                attrs={
                    'readonly': True,
                    'class': 'form-control select2',
                }
            ),
            'fichaTrabajo': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'INGRESE UNA FICHA DE TRABAJO',
                # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                'style': 'text-transform: uppercase'
            }),
            'observaciones': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'INGRESE UNA OBSERVACIÓN',
                # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                'style': 'text-transform: uppercase'
            }),
        }
        exclude = ['usuario', 'estado']


class PlanificacionesSemanalesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PlanificacionesSemanales
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'INGRESE UN NOMBRE',
                # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                'style': 'text-transform: uppercase'
            }),
            'fechaInicio': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'fechaInicio',
                    'data-target': '#fechaInicio',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'fechaFin': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'fechaFin',
                    'data-target': '#fechaFin',
                    'data-toggle': 'datetimepicker'
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