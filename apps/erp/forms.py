from django.forms import ModelForm, TextInput, Select, BooleanField

from apps.erp.models import Categorias, Subcategorias, Productos


class CategoriasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categorias
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'abreviatura': TextInput(
                attrs={
                    'placeholder': 'Ingrese una abreviatura',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
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


class SubcategoriasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].widget.attrs['autofocus'] = True

    class Meta:
        model = Subcategorias
        fields = '__all__'
        widgets = {
            'categoria': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'abreviatura': TextInput(
                attrs={
                    'placeholder': 'Ingrese una abreviatura',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
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


class ProductosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategoria'].widget.attrs['autofocus'] = True

    class Meta:
        model = Productos
        fields = '__all__'
        widgets = {
            'subcategoria': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'abreviatura': TextInput(
                attrs={
                    'placeholder': 'Ingrese una abreviatura',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigo': TextInput(
                attrs={
                    'placeholder': 'Ingrese un código de producto',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigoBarras1': TextInput(
                attrs={
                    'placeholder': 'Ingrese un código de Barras',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigoBarras2': TextInput(
                attrs={
                    'placeholder': 'Ingrese un código de Barras',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigoProveedor': TextInput(
                attrs={
                    'placeholder': 'Ingrese un código de proveedor',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'iva': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'ubicacion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una ubicación de producto',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'observaciones': TextInput(
                attrs={
                    'placeholder': 'Ingrese unas observaciones',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'stockReal': TextInput(attrs={
                'class': 'form-control',
            }),
            'stockMinimo': TextInput(attrs={
                'class': 'form-control',
            }),
            'reposicion': TextInput(attrs={
                'class': 'form-control',
            }),
            'costo': TextInput(attrs={
                'class': 'form-control',
            }),
            'utilidad': TextInput(attrs={
                'class': 'form-control',
            }),
            'precioVenta': TextInput(attrs={
                'class': 'form-control',
            }),
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