from django.forms import ModelForm, Select, TextInput, DateInput

from apps.presupuestos.models import PresupuestosBase, Presupuestos


class PresupuestosBaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PresupuestosBase
        fields = '__all__'
        widgets = {
            'modelo': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'descripcion': TextInput(attrs={
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }


class PresupuestosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                'readonly': True,
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
                'placeholder': 'INGRESE UNA OBSERVACIÓN',
                'class': 'form-control',
            }),
        }
        exclude = ['usuario']
