import json
import datetime
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from weasyprint import HTML, CSS

from apps.parametros.models import Empresa
from apps.pedidos.forms import PedidoSolicitudProveedorForm
from apps.pedidos.models import PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor, DetallePedidoSolicitud, \
    PedidosSolicitud
from apps.mixins import ValidatePermissionRequiredMixin

from django.urls import reverse

from config import settings


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
            elif action == 'search_detalle_cotización':
                data = []
                for i in DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Solicitudes de Pedidos por Proveedor'
        context['list_url'] = reverse_lazy('pedidos:pedidos_solicitudes_proveedores_list')
        context['entity'] = 'Solicitudes de Pedidos por Proveedor'
        return context


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
                            item['marcaOfertada'] = ""
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
                        # Guardamos los importes de la cabecera
                        pedidoP.subtotal = float(formPedidoRequest['subtotal'])
                        pedidoP.iva = float(formPedidoRequest['iva'])
                        pedidoP.total = float(formPedidoRequest['total'])
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
                        data = {'id': pedidoP.id}
                        data['redirect'] = reverse('pedidos:pedidos_solicitudes_correcto')
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


class PedidosSolicitudProveedoresPdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Armamos el Logo de la Empresa
            logo = "file://" + str(settings.MEDIA_ROOT) + str(empresa.imagen)
            # Obtenemos la Solicitud del Proveedor para acceder al detalle
            cotizacionProveedor = PedidoSolicitudProveedor.objects.get(id=self.kwargs['pk'])
            print(cotizacionProveedor.detallepedidosolicitudproveedor_set)
            # Obtenemos la Solicitud de Cotizacion a la cual pertenece el Pedido para obtener los datos de Cabecera
            pedidoSolicitud = PedidosSolicitud.objects.get(id=cotizacionProveedor.pedidoSolicitud.id)
            print(cotizacionProveedor.respuesta)
            # Utilizamos el template para generar el PDF
            template = get_template('pedidosSolicitudProveedores/pdf.html')
            context = {
                'pedido': pedidoSolicitud,
                'cotizacion': cotizacionProveedor,
                'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                            'localidad': empresa.localidad.get_full_name(), 'imagen': logo},
            }
            # Generamos el render del contexto
            html = template.render(context)
            # Asignamos la ruta del CSS de BOOTSTRAP
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            # Creamos el PDF
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('pedidos:pedidos_solicitudes_correcto'))


class ExpiredSolicitudProveedorView(TemplateView):
    template_name = 'pedidosSolicitudProveedores/expired.html'


class CorrectoSolicitudProveedorView(TemplateView):
    template_name = 'pedidosSolicitudProveedores/correct.html'
