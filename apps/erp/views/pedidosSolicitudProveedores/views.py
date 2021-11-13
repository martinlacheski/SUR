import json
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.erp.forms import ProductosForm, PedidoSolicitudProveedorForm
from apps.erp.models import Productos, Categorias, Subcategorias, PedidosSolicitud, DetallePedidoSolicitud, \
    PedidoSolicitudProveedor, DetallePedidoSolicitudProveedor
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import  TiposIVA



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


class PedidosSolicitudProveedoresCreateView(CreateView): #Da totalmente igual qué tipo de view es
    model = PedidoSolicitudProveedor
    form_class = PedidoSolicitudProveedorForm
    template_name = 'pedidosSolicitudProveedores/create.html'
    success_url = reverse_lazy('erp:pedidos_solicitudes_proveedores_list')
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        #print(self.kwargs['hash_code'])
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_productos_pedidos':
                data = []
                pedidoP = PedidoSolicitudProveedor.objects.get(hash=self.kwargs['hash_code'])
                # Acá agarra los objetos con el stock minimo
                for det in DetallePedidoSolicitudProveedor.objects.filter(pedidoSolicitudProveedor=pedidoP):
                    item = det.producto.toJSON()
                    item['cantidad'] = det.producto.reposicion
                    data.append(item)
                cabecera = {}
                cabecera['pedido'] = pedidoP.pedidoSolicitud.id
                cabecera['proveedor'] = {'id': pedidoP.proveedor.id,
                                     'text': pedidoP.proveedor.razonSocial}
                data.append(cabecera)
            # Buscamos los distintos productos ingresando por teclado excluyendo ya cargados
            # Buscamos el IVA para el MODAL de Productos

            elif action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            # Select Anidado de Categorias
            elif action == 'search_subcategorias':
                data = [{'id': '', 'text': '---------'}]
                for i in Subcategorias.objects.filter(categoria_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            # si no existe el Producto lo creamos
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # ACTUALIZACION DE PRECIO
            elif action == 'update_precioProducto':
                with transaction.atomic():
                    producto = Productos.objects.get(id=request.POST['pk'])
                    producto.costo = float(request.POST['costo'])
                    producto.utilidad = float(request.POST['utilidad'])
                    producto.precioVenta = float(request.POST['precioVenta'])
                    producto.save()
            # Buscamos el Precio del Producto luego de actualizar el precio
            elif action == 'search_precioProducto':
                producto = Productos.objects.get(id=request.POST['pk'])
                data = producto.costo
            elif action == 'add':
                with transaction.atomic():
                    formPedidoRequest = json.loads(request.POST['pedido'])
                    pedido = PedidosSolicitud()
                    pedido.fecha = formPedidoRequest['fecha']
                    pedido.fechaLimite = formPedidoRequest['fechaLimite']
                    pedido.subtotal = float(formPedidoRequest['subtotal'])
                    pedido.iva = float(formPedidoRequest['iva'])
                    pedido.total = float(formPedidoRequest['total'])
                    pedido.save()
                    for i in formPedidoRequest['productos']:
                        det = DetallePedidoSolicitud()
                        det.pedido_id = pedido.id
                        try:
                            det.proveedor_id = i['proveedor']
                        except:
                            pass
                        det.producto_id = i['id']
                        det.costo = float(i['costo'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Devolvemos en Data la ID del nuevo pedido para poder generar la Boleta
                    data = {'id': pedido.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Completar Solicitud de Pedido'
        context['entity'] = 'Solicitudes de Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['categorias'] = Categorias.objects.all()
        context['formProducto'] = ProductosForm()
        return context

