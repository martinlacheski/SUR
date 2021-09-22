from django.forms import ModelForm, Select, TextInput

from apps.presupuestos.models import PresupuestosBase


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
