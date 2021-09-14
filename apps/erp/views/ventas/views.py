import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.erp.forms import VentasForm, ClientesForm
from apps.erp.models import Ventas, Productos, Servicios, DetalleProductosVenta, DetalleServiciosVenta, Clientes
from apps.mixins import ValidatePermissionRequiredMixin


class VentasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('erp:ventas_list')
    permission_required = 'erp.add_venta'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create_cliente':
                with transaction.atomic():
                    formCliente = ClientesForm(request.POST)
                    data = formCliente.save()

            elif action == 'search_productos':
                data = []
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                productos = Productos.objects.filter(
                    Q(descripcion__icontains=term) | Q(codigo__icontains=term) | Q(codigoProveedor__icontains=term)
                    | Q(codigoBarras1__icontains=term) | Q(codigoBarras2__icontains=term))[0:10]
                for i in productos[0:10]:
                    item = i.toJSON()
                    # Creamos un item VALUE para que reconozca el input de Busqueda
                    item['value'] = i.descripcion
                    data.append(item)
            elif action == 'search_servicios':
                data = []
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                servicios = Servicios.objects.filter(
                    Q(descripcion__icontains=term) | Q(codigo__icontains=term))[0:10]
                for i in servicios[0:10]:
                    item = i.toJSON()
                    # Creamos un item VALUE para que reconozca el input de Busqueda
                    item['value'] = i.descripcion
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    ventas = json.loads(request.POST['ventas'])
                    venta = Ventas()
                    venta.fecha = ventas['fecha']
                    venta.tipoComprobante_id = ventas['tipoComprobante']
                    venta.cliente_id = ventas['cliente']
                    venta.condicionPago_id = ventas['condicionPago']
                    venta.subtotal = float(ventas['subtotal'])
                    venta.iva = float(ventas['iva'])
                    venta.percepcion = float(ventas['percepcion'])
                    venta.total = float(ventas['total'])
                    venta.save()
                    for i in ventas['productos']:
                        det = DetalleProductosVenta()
                        det.venta_id = venta.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.producto.stockReal -= det.cantidad
                        det.producto.save()
                    for i in ventas['servicios']:
                        det = DetalleServiciosVenta()
                        det.venta_id = venta.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': venta.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['formCliente'] = ClientesForm()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context
