from django.forms import ModelForm, TextInput, Select, PasswordInput, SelectMultiple, DateInput, EmailInput
from django.urls import reverse_lazy

from apps.usuarios.models import TiposUsuarios, Usuarios


class TiposUsuariosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = TiposUsuarios
        fields = ['nombre']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
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

    """ Chequea si ya existe y avisa al front-end.
        También controla duplicados al momento de editar """

    def checkAndSave(self, form, url_redirect, action):
        data = {}
        if form.is_valid():
            # Si existe el objeto que se quiere guardar/editar y está activo, error.
            try:
                tipoUsuario = TiposUsuarios.objects.get(nombre=form.cleaned_data['nombre'].upper())
                data['check'] = True
            except Exception as e:
                if action == 'add':
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()
                # action 'edit'
                elif action == 'edit':
                    data['check'] = 'Registrar'
                    data['redirect'] = url_redirect
                    form.save()

        else:
            data['error'] = "Formulario no válido"
        return data


class UsuariosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuarios
        # fields = '__all__'
        fields = 'first_name', 'last_name', 'username', 'password', 'email', 'legajo', 'fechaIngreso', 'cuil', \
                 'localidad', 'direccion', 'telefono', 'groups', 'imagen'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el apellido',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre de Usuario',
                }
            ),
            'password': PasswordInput(render_value=True,
                                      attrs={
                                          'placeholder': 'Ingrese una contraseña',
                                          'style': 'width: 100%'
                                      }
                                      ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese un correo electrónico válido',
                    'style': 'width: 100%'
                }
            ),
            'legajo': TextInput(
                attrs={
                    'placeholder': 'Ingrese un legajo',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'fechaIngreso': DateInput(
                attrs={
                    'placeholder': 'Seleccione la fecha de ingreso',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_reserva',
                    'data-target': '#fechaIngreso',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'cuil': TextInput(
                attrs={
                    'placeholder': 'Ingrese un CUIL',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'localidad': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una dirección',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese un número de teléfono',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'groups': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }
            )
            # 'tipoUsuario': Select(
            #     attrs={
            #         'class': 'form-control select2',
            #         'style': 'width: 100%'
            #     }
            # ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']

                # PASAMOS A MAYUSCULAS LOS CAMPOS PARA GUARDAR EN LA BD
                self.cleaned_data['first_name'] = self.cleaned_data['first_name'].upper()
                self.cleaned_data['last_name'] = self.cleaned_data['last_name'].upper()
                self.cleaned_data['direccion'] = self.cleaned_data['direccion'].upper()

                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)

                    #llamamos al metodo en models para pasar a mayusculas antes de guardar
                    u.saveCreate()
                else:
                    user = Usuarios.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)

                    #Utilizamos el SAVE convencional, porque el paso a mayuscula viene de la VIEW
                    u.save()

                # limpiar los grupos que tiene el usuario
                u.groups.clear()

                # cargar los grupos que tiene el usuario
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
