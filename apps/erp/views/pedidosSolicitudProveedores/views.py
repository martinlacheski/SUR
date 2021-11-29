import json
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from apps.erp.forms import ProductosForm, PedidoSolicitudProveedorForm
from apps.erp.models import Productos, Categorias, Subcategorias, PedidosSolicitud, DetallePedidoSolicitud, \
    PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import  TiposIVA
from django.utils import timezone
from django.core.exceptions import *
from django.urls import reverse



class PedidosSolicitudProveedoresListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView, ):
    model = PedidoSolicitudProveedor
    template_name = 'pedidosSolicitudProveedores/list.html'
    permission_required = 'erp.view_pedidosolicitudproveedor'

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
        #context['create_url'] = reverse_lazy('erp:pedidos_solicitudes_proveedores_create')
        context['list_url'] = reverse_lazy('erp:pedidos_solicitudes_proveedores_list')
        context['entity'] = 'Solicitudes de Pedidos por Proveedor'
        return context

#
class PedidosSolicitudProveedoresCreateView(CreateView): #Da totalmente igual qué tipo de view es
    model = PedidoSolicitudProveedor
    form_class = PedidoSolicitudProveedorForm
    template_name = 'pedidosSolicitudProveedores/create.html'
    success_url = reverse_lazy('erp:pedidos_solicitudes_proveedores_list')
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pedidoP = PedidoSolicitudProveedor.objects.get(hash=self.kwargs['hash_code'])

        if pedidoP.pedidoSolicitud.fechaLimite >= timezone.now():
            try:
                # Obtenemos la cabecera del Pedido
                if action == 'search_cabecera':
                    data['pedido'] = pedidoP.pedidoSolicitud.id
                    data['proveedor'] = pedidoP.proveedor.razonSocial
                    data['validoHasta'] = pedidoP.pedidoSolicitud.fechaLimite
                    # Marcamos vista del pedido
                    pedidoP.visto = timezone.now()
                    pedidoP.save()

                # Obtenemos el Detalle del Pedido
                elif action == 'get_productos_pedidos':
                    data = []
                    if pedidoP.pedidoSolicitud.fechaLimite >= timezone.now():
                        for det in DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=pedidoP):
                            item = det.producto.toJSON()
                            item['cantidad'] = det.producto.reposicion
                            data.append(item)


                elif action == 'add':   # TO-DO: se tiene que cambiar el nombre de la acción en el front end
                    with transaction.atomic():
                        formPedidoRequest = json.loads(request.POST['pedido'])

                        # Guaradamos respuesta
                        pedidoP.respuesta = timezone.now()
                        pedidoP.save()

                        #Borramos detalle actual
                        for dp in DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=pedidoP):
                            dp.delete()

                        # Lo actualizamos
                        for i in formPedidoRequest['productos']:
                            detSP = DetallePedidoSolicitudProveedor()
                            detSP.pedidoSolicitudProveedor = pedidoP
                            detSP.producto = Productos.objects.get(pk=i['id'])
                            detSP.costo = float(i['costo'])
                            detSP.subtotal = float(i['subtotal'])
                            detSP.cantidad = int(i['cantidad'])
                            detSP.save()

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
                        #data = {'id': pedido.id}
                        data['redirect'] = self.url_redirect
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            data['redirect'] = reverse('erp:pedidos_solicitudes_expired')
            print(data)
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



