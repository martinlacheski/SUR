from django.forms import ModelForm, TextInput, Select, PasswordInput, SelectMultiple, DateInput, EmailInput, \
    CheckboxInput
from apps.usuarios.models import Usuarios
from django.contrib.auth.models import Group


class GruposUsuariosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
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


class UsuariosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuarios
        # fields = '__all__'
        fields = 'first_name', 'last_name', 'username', 'password', 'email', 'legajo', 'fechaIngreso', 'cuil', \
                 'localidad', 'direccion', 'telefono', 'groups', 'imagen', 'is_active', 'is_superuser'
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
            ),
            'is_superuser': CheckboxInput(
                attrs={
                    'type': 'checkbox',
                    'class': 'custom-control-input',
                }
            ),
            'is_active': CheckboxInput(
                attrs={
                    'type': 'checkbox',
                    'class': 'custom-control-input',
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_staff',
                   'chatIdUsuario']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                # PASAMOS A MAYUSCULAS LOS CAMPOS PARA GUARDAR EN LA BD
                self.cleaned_data['first_name'] = self.cleaned_data['first_name'].upper()
                self.cleaned_data['last_name'] = self.cleaned_data['last_name'].upper()
                self.cleaned_data['direccion'] = self.cleaned_data['direccion'].upper()
                if u.pk is None:
                    u.set_password(pwd)
                    # llamamos al metodo en models para pasar a mayusculas antes de guardar
                    u.saveCreate()
                    # u.save()
                else:
                    user = Usuarios.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                    # Utilizamos el SAVE convencional, porque el paso a mayuscula viene de la VIEW
                    u.save()
                # limpiar los grupos que tiene el usuario
                u.groups.clear()
                # cargar los grupos que tiene el usuario
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
                # print(form.errors)
        except Exception as e:
            data['error'] = str(e)
        return data


class UsuariosProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuarios
        fields = 'first_name', 'last_name', 'username', 'password', 'email', 'cuil', \
                 'localidad', 'direccion', 'telefono', 'imagen'
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
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = Usuarios.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
