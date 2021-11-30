from django.forms import ModelForm, TextInput, Select, EmailInput, DateInput, DateTimeInput, CheckboxInput

from apps.erp.models import Categorias, Subcategorias, Productos, Servicios, Clientes, Proveedores, Ventas, Compras, \
    PedidosSolicitud, PedidoSolicitudProveedor


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
                # Obtenemos la INSTANCIA AL GUARDAR PARA OBTENER EL OBJETO Y PASAR AL SELECT2
                instance = form.save()
                data = instance.toJSON()
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
                # Obtenemos la INSTANCIA AL GUARDAR PARA OBTENER EL OBJETO Y PASAR AL SELECT2
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['subcategoria'].widget.attrs['autofocus'] = True
        # Inicializamos el Select2 vacio
        # self.fields['subcategoria'].queryset = Subcategorias.objects.none()

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
                    'placeholder': 'Ingrese descripción',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'abreviatura': TextInput(
                attrs={
                    'placeholder': 'Ingrese abreviatura',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigo': TextInput(
                attrs={
                    'placeholder': 'Ingrese código producto',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigoBarras1': TextInput(
                attrs={
                    'placeholder': 'Ingrese código de Barras',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigoBarras2': TextInput(
                attrs={
                    'placeholder': 'Ingrese código de Barras',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigoProveedor': TextInput(
                attrs={
                    'placeholder': 'Ingrese código proveedor',
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
                    'placeholder': 'Ingrese ubicación producto',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'observaciones': TextInput(
                attrs={
                    'placeholder': 'Ingrese observaciones',
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
            'esInsumo': CheckboxInput(
                attrs={
                    'type': 'checkbox',
                    'class': 'custom-control-input',
                }
            ),
            'descuentaStock': CheckboxInput(
                attrs={
                    'type': 'checkbox',
                    'class': 'custom-control-input',
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


class ServiciosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Servicios
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'codigo': TextInput(
                attrs={
                    'placeholder': 'Ingrese un código',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'iva': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'costo': TextInput(attrs={
                'class': 'form-control',
            }),
            'precioVenta': TextInput(attrs={
                'class': 'form-control',
            }),
            'esfuerzo': TextInput(attrs={
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


class ClientesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['razonSocial'].widget.attrs['autofocus'] = True
        # Desactivamos los campos al inicializar el formulario
        self.fields['limiteCtaCte'].widget.attrs['disabled'] = True
        self.fields['plazoCtaCte'].widget.attrs['disabled'] = True

    class Meta:
        model = Clientes
        fields = '__all__'
        widgets = {
            'razonSocial': TextInput(
                attrs={
                    'placeholder': 'INGRESE UNA RAZÓN SOCIAL',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'condicionIVA': Select(attrs={
                'class': 'form-control select2',
            }),
            'cuil': TextInput(
                attrs={
                    'placeholder': 'INGRESE UN CUIL-CUIT',
                }
            ),
            'localidad': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'INGRESE UNA DIRECCIÓN',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'INGRESE NÚMERO DE TELÉFONO',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'INGRESE CORREO ELECTRÓNICO VÁLIDO',
                    'style': 'width: 100%'
                }
            ),
            'cbu': TextInput(
                attrs={
                    'placeholder': 'INGRESE UN CBU/CVU',
                }
            ),
            'alias': TextInput(
                attrs={
                    'placeholder': 'INGRESE UN ALIAS',
                }
            ),
            'tipoPercepcion': Select(attrs={
                'class': 'form-control select2',
            }),
            'condicionPago': Select(attrs={
                'class': 'form-control select2',
            }),
            'limiteCtaCte': TextInput(attrs={
                'class': 'form-control',
            }),
            'plazoCtaCte': TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # Obtenemos la INSTANCIA AL GUARDAR PARA OBTENER EL OBJETO Y PASAR AL SELECT2
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProveedoresForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['razonSocial'].widget.attrs['autofocus'] = True
        # Desactivamos los campos al inicializar el formulario
        self.fields['plazoCtaCte'].widget.attrs['disabled'] = True

    class Meta:
        model = Proveedores
        fields = '__all__'
        widgets = {
            'razonSocial': TextInput(
                attrs={
                    'placeholder': 'INGRESE UNA RAZÓN SOCIAL',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase',
                }
            ),
            'condicionIVA': Select(attrs={
                'class': 'form-control select2',
            }),
            'cuit': TextInput(
                attrs={
                    'placeholder': 'INGRESE UN CUIT',
                }
            ),
            'localidad': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'INGRESE UNA DIRECCIÓN',
                    # agregamos este estilo para que convierta lo que ingresamos a mayuscula
                    'style': 'text-transform: uppercase'
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'INGRESE NÚMERO DE TELÉFONO',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'INGRESE CORREO ELECTRÓNICO VÁLIDO',
                    'style': 'width: 100%'
                }
            ),
            'cbu': TextInput(
                attrs={
                    'placeholder': 'INGRESE UN CBU/CVU',
                }
            ),
            'alias': TextInput(
                attrs={
                    'placeholder': 'INGRESE UN ALIAS',
                }
            ),
            'tipoPercepcion': Select(attrs={
                'class': 'form-control select2',
            }),
            'condicionPago': Select(attrs={
                'class': 'form-control select2',
            }),
            'plazoCtaCte': TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # Obtenemos la INSTANCIA AL GUARDAR PARA OBTENER EL OBJETO Y PASAR AL SELECT2
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class VentasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Ventas
        fields = '__all__'
        widgets = {
            'condicionVenta': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'medioPago': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'cliente': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'fecha': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'percepcion': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }
        exclude = ['usuario']


class ComprasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Compras
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
            'condicionPagoCompra': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'proveedor': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'tipoComprobante': Select(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'nroComprobante': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un número de comprobante',
                }
            ),
            'iva': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'percepcion': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }
        exclude = ['usuario']


class PedidosSolicitudForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PedidosSolicitud
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
            'fechaLimite': DateTimeInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'fechaLimite',
                    'data-target': '#fechaLimite',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }
        exclude = ['estado']


class PedidoSolicitudProveedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PedidoSolicitudProveedor
        fields = '__all__'
        widgets = {
            'pedidoSolicitud': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'proveedor': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'iva': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }