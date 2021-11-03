

from django.forms import ModelForm, Textarea, Select, CheckboxInput, TextInput, TimeInput, DateInput, DateField

from apps.agenda.models import *
from django import forms



class GestionEventosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    fechaNotificacion = forms.DateField(
        input_formats=['%d-%m-%Y'],

        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#fechaNotificacion',
            'data-toggle': 'datetimepicker',
            'autocomplete': 'off',
            # 'data-format': 'DD-MM-yyyy',
        })
    )

    fechaFinalizacion = forms.DateField(
        input_formats=['%d-%m-%Y'],
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#fechaFinalizacion',
            'data-toggle': 'datetimepicker',
            'autocomplete': 'off',
        })
    )

    class Meta:
        model = eventosAgenda
        fields = ['tipoEvento', 'descripcion', 'fechaNotificacion', 'repeticion', 'fechaFinalizacion']
        widgets = {
            'tipoEvento': Select(attrs={
                'class': 'form-select form-control select2',
            }),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Describa su evento',
                    'rows': '3',
                    'class': 'form-control',
                    'style': 'text-transform: uppercase',
                }

            ),
            # 'fechaNotificacion': DateInput(
            #     attrs={
            #         'class': 'form-control datetimepicker-input',
            #         'data-target': '#fechaNotificacion',
            #         'data-toggle': 'datetimepicker',
            #         'autocomplete': 'off',
            #     }
            # ),
            'repeticion' : Select(
                attrs={
                    'class' : 'form-select form-control select2',
                    'id' : 'selectRepeticion',
                    'disabled' : '',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                eventoObj = form.save()
                data['eventoObj'] = eventoObj
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class GestionTiposEventosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = tiposEvento
        fields = ['nombre', 'horarioRecordatorio', 'recordarSistema', 'recordarTelegram']

        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un tipo de evento',
                    'style': 'text-transform: uppercase',
                    'type': 'text',
                    'class': 'form-control'
                }
            ),
            'horarioRecordatorio': TimeInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#timepicker',
                    'type':'text'
                }
            ),
            'recordarSistema': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
                }
            ),
            'recordarTelegram': CheckboxInput(
                attrs={
                    'type': 'checkbox',
                    'class': 'custom-control-input',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        if form.is_valid():
            try:
                data['obj'] = form.save()
            except Exception as e:
                data['error'] = str(e)
        else:
            data['error'] = form.errors
        return data


class GestionNotifEventosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = diasAvisoEvento
        fields = ['diasAntelacion', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

        widgets = {
            'diasAntelacion': TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lunes': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
                }
            ),
            'martes': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
                }
            ),
            'miercoles': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
                }
            ),
            'jueves': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
                }
            ),
            'viernes': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
                }
            ),
            'sabado': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
                }
            ),
            'domingo': CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class':'custom-control-input',
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
