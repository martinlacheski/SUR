from django.forms import ModelForm, Textarea, Select, DateTimeField, CheckboxInput, TimeField, TextInput, TimeInput
from apps.agenda.models import *
from django import forms

class GestionEventosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

                }
            ),
            'recordarTelegram': CheckboxInput(
                attrs={

                }
            ),
            'recordarEmail': CheckboxInput(
                attrs={

                }
            ),
            'usuarioNotif': Select(
                attrs={
                    'class' : 'form-control'
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