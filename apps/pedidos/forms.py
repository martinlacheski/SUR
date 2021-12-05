from django.forms import ModelForm, TextInput, DateInput, DateTimeInput

from apps.pedidos.models import PedidosSolicitud, PedidoSolicitudProveedor, Pedidos


class PedidosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Pedidos
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