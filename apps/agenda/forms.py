

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
            'data-target': '#fechaNotificacio',
            'data-toggle': 'datetimepicker'
        })
    )

    class Meta:
        model = eventosAgenda
        fields = ['tipoEvento', 'descripcion', 'fechaNotificacion', 'repeticion']
        widgets = {
            'tipoEvento': Select(attrs={
                'class': 'form-select form-control select2',
            }),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Describa su evento',
                    'rows': '3',
                    'class': 'form-control',

                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }

            ),
            # 'fechaNotificacion': DateInput(
            #     attrs={
            #         'class': 'form-control datetimepicker-input',
            #         'data-target': '#fechaNotificacio',
            #         'data-toggle': 'datetimepicker'
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
                form.save()
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
        fields = ['nombre', 'horarioRecordatorio', 'usuarioNotif', 'recordarSistema', 'recordarTelegram', 'recordarEmail']

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
            'recordarEmail': CheckboxInput(
                attrs={
                    'type': 'checkbox',
                    'class': 'custom-control-input',
                }
            ),
            'usuarioNotif': Select(
                attrs={
                    'class' : 'form-select form-control select2',
                    'required': '',
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

    """ Chequea si el pais ya existe y avisa al front-end.
        Si el pais que se ingresa estaba de baja, lo da de alta.
        También controla duplicados al momento de editar """

# Por el momento no se hará chequeo de repetidos
#     def checkAndSave(self, form, url_redirect, action):
#         data = {}
#         if form.is_valid():
#             # Si existe el pais que se quiere guardar/editar y está activo, error.
#             try:
#                 pais = Paises.objects.get(nombre=form.cleaned_data['nombre'].upper())
#                 data['check'] = True
#             except Exception as e:
#                 if action == 'add':
#                     data['check'] = 'Registrar'
#                     data['redirect'] = url_redirect
#                     form.save()
#                 # action 'edit'
#                 elif action == 'edit':
#                     data['check'] = 'Registrar'
#                     data['redirect'] = url_redirect
#                     form.save()
#
#         else:
#             data['error'] = "Formulario no válido"
#         return data