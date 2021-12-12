from django.forms import ModelForm, Select, TextInput, DateInput

from apps.erp.models import Clientes
from apps.presupuestos.models import PlantillaPresupuestos, Presupuestos


class PresupuestosPlantillaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PlantillaPresupuestos
        fields = '__all__'
        widgets = {
            'modelo': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'descripcion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'INGRESE UNA DESCRIPCIÓN',
                # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                'style': 'text-transform: uppercase'
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }


class PresupuestosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.filter(estado=True)

    class Meta:
        model = Presupuestos
        fields = '__all__'
        widgets = {
            'fecha': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'validez': TextInput(attrs={
                'class': 'form-control',
            }),
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
            'observaciones': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'INGRESE UNA OBSERVACIÓN',
                # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                'style': 'text-transform: uppercase'
            }),
        }
        exclude = ['usuario']
