from django.forms import ModelForm, Textarea, Select, DateTimeField, CheckboxInput
from apps.agenda.models import *
from django import forms

class GestionEventosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Seteamos para que el Select contenga unicamente los registros activos
        # self.fields['pais'].widget.attrs['autofocus'] = True


    fechaNotificacion = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#reservationdatetime'
        })
    )

    class Meta:
        model = eventosAgenda
        fields = ['tipoEvento', 'descripcion', 'fechaNotificacion', 'repeticion']
        widgets = {
            'tipoEvento': Select(attrs={
                'class': 'form-control',
            }),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Describa su evento',
                    'rows' : '3',
                    'class' : 'form-control',

                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }

            ),
            'repeticion' : Select(
                attrs={
                    'class' : 'form-control',
                    'id' : 'selectRepeticion',
                    'disabled' : '',
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


