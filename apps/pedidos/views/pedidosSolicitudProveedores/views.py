import json
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from apps.erp.models import Productos
from apps.pedidos.forms import PedidoSolicitudProveedorForm
from apps.pedidos.models import PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor, DetallePedidoSolicitud
from apps.mixins import ValidatePermissionRequiredMixin

from django.urls import reverse


class PedidosSolicitudProveedoresListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView, ):
    model = PedidoSolicitudProveedor
    template_name = 'pedidosSolicitudProveedores/list.html'
    permission_required = 'pedidos.view_pedidosolicitudproveedor'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in PedidoSolicitudProveedor.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Solicitudes de Pedidos por Proveedor'
        # context['create_url'] = reverse_lazy('pedidos:pedidos_solicitudes_proveedores_create')
        context['list_url'] = reverse_lazy('pedidos:pedidos_solicitudes_proveedores_list')
        context['entity'] = 'Solicitudes de Pedidos por Proveedor'
        return context


#
class PedidosSolicitudProveedoresCreateView(CreateView):  # Da totalmente igual qué tipo de view es
    model = PedidoSolicitudProveedor
    form_class = PedidoSolicitudProveedorForm
    template_name = 'pedidosSolicitudProveedores/create.html'
    success_url = reverse_lazy('pedidos:pedidos_solicitudes_proveedores_list')
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pedidoP = PedidoSolicitudProveedor.objects.get(hash=self.kwargs['hash_code'])
        fechaLimite = pedidoP.pedidoSolicitud.fechaLimite
        fechaLimite = datetime.datetime(fechaLimite.year, fechaLimite.month, fechaLimite.day,
                               fechaLimite.hour, fechaLimite.minute, fechaLimite.second)
        if action == 'search_validez':
            if fechaLimite >= datetime.datetime.today():
                data['ok'] = 'si'
            else:
                data['ok'] = 'no'
                data['redirect'] = reverse('pedidos:pedidos_solicitudes_expired')
        if fechaLimite >= datetime.datetime.today():
            try:
                # Obtenemos la cabecera del Pedido
                if action == 'search_cabecera':
                    data['pedido'] = pedidoP.pedidoSolicitud.id
                    data['proveedor'] = pedidoP.proveedor.razonSocial
                    data['validoHasta'] = pedidoP.pedidoSolicitud.fechaLimite
                    # Marcamos vista del pedido
                    pedidoP.visto = datetime.datetime.now()
                    pedidoP.save()
                # Obtenemos el Detalle del Pedido
                elif action == 'get_productos_pedidos':
                    data = []
                    for i in DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=pedidoP):
                        item = i.producto.toJSON()
                        item['marcaOfertada'] = i.marcaOfertada
                        item['cantidad'] = i.cantidad
                        item['costo'] = i.costo
                        data.append(item)
                # Reseteamos formulario con lo solicitado en la solicitud original
                elif action == 'resetear_formulario':
                    data = []
                    try:
                        for i in DetallePedidoSolicitud.objects.filter(
                                pedido=request.POST['pk']):
                            item = i.producto.toJSON()
                            item['marcaOfertada'] = i.marcaOfertada
                            item['cantidad'] = i.cantidad
                            item['precio'] = i.producto.costo
                            data.append(item)
                    except Exception as e:
                        data['error'] = str(e)
                elif action == 'add':  # TO-DO: se tiene que cambiar el nombre de la acción en el front end
                    with transaction.atomic():
                        formPedidoRequest = json.loads(request.POST['pedido'])
                        # Guardamos respuesta
                        pedidoP.respuesta = datetime.datetime.now()
                        pedidoP.save()
                        # Eliminamos todos los productos del Detalle
                        pedidoP.detallepedidosolicitudproveedor_set.all().delete()
                        # Volvemos a cargar los productos al Detalle
                        for i in formPedidoRequest['productos']:
                            det = DetallePedidoSolicitudProveedor()
                            det.pedidoSolicitudProveedor_id = pedidoP.id
                            det.producto_id = i['id']
                            det.marcaOfertada = i['marcaOfertada']
                            det.cantidad = int(i['cantidad'])
                            det.costo = float(i['costo'])
                            det.subtotal = float(i['subtotal'])
                            det.save()
                        data['redirect'] = reverse('pedidos:pedidos_solicitudes_correcto')
                        # Borramos detalle actual
                        # for dp in DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=pedidoP):
                        #     dp.delete()
                        # Lo actualizamos
                        # for i in formPedidoRequest['productos']:
                        #     print()
                        #     detSP = DetallePedidoSolicitudProveedor()
                        #     detSP.pedidoSolicitudProveedor = pedidoP
                        #     detSP.producto = Productos.objects.get(pk=i['id'])
                        #     detSP.costo = float(i['costo'])
                        #     detSP.subtotal = float(i['subtotal'])
                        #     detSP.cantidad = int(i['cantidad'])
                        #     detSP.save()
                        # det.pedido_id = pedido.id
                        # try:
                        #     det.proveedor_id = i['proveedor']
                        # except:
                        #     pass
                        # det.producto_id = i['id']
                        # det.costo = float(i['costo'])
                        # det.cantidad = int(i['cantidad'])
                        # det.subtotal = float(i['subtotal'])
                        # det.save()
                        # Devolvemos en Data la ID del nuevo pedido para poder generar la Boleta
                        # data = {'id': pedido.id}
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            data['ok'] = 'no'
            data['redirect'] = reverse('pedidos:pedidos_solicitudes_expired')
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Completar Solicitud de Pedido'
        context['entity'] = 'Solicitudes de Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ExpiredSolicitudProveedorView(TemplateView):
    template_name = 'pedidosSolicitudProveedores/expired.html'


class CorrectoSolicitudProveedorView(TemplateView):
    template_name = 'pedidosSolicitudProveedores/correct.html'
