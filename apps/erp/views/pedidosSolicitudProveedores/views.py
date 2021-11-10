import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.erp.forms import ProductosForm, PedidosSolicitudForm, PedidoSolicitudProveedorForm
from apps.erp.models import Productos, Categorias, Subcategorias, PedidosSolicitud, \
    DetallePedidoSolicitud, PedidoSolicitudProveedor
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import  TiposIVA



class PedidosSolicitudProveedoresListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
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
        context['create_url'] = reverse_lazy('erp:pedidos_solicitudes_create')
        context['list_url'] = reverse_lazy('erp:pedidos_solicitudes_list')
        context['entity'] = 'Solicitudes de Pedidos por Proveedor'
        return context


class PedidosSolicitudProveedoresCreateView(CreateView):
    model = PedidoSolicitudProveedor
    form_class = PedidoSolicitudProveedorForm
    template_name = 'pedidosSolicitudProveedores/create.html'
    success_url = reverse_lazy('erp:pedidos_solicitudes_proveedores_list')
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_productos_pedidos':
                data = []
                # Acá agarra los objetos con el stock minimo
                for producto in Productos.objects.all():
                    if producto.stockReal < producto.stockMinimo and producto.reposicion > 0:
                        item = producto.toJSON()
                        item['cantidad'] = producto.reposicion
                        data.append(item)
            # Buscamos los distintos productos ingresando por teclado excluyendo ya cargados
            elif action == 'search_productos':
                data = []
                term = request.POST['term'].strip()
                ids_exclude = json.loads(request.POST['excluir'])
                try:
                    data.append({'id': term, 'text': term})
                    productos = Productos.objects.filter(
                        Q(descripcion__icontains=term) | Q(codigo__icontains=term) | Q(codigoProveedor__icontains=term)
                        | Q(codigoBarras1__icontains=term)).exclude(id__in=ids_exclude)[0:10]
                    for i in productos[0:10]:
                        item = i.toJSON()
                        # Creamos un item VALUE para que reconozca el input de Busqueda
                        item['value'] = i.descripcion
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            # Metodo para obtener un producto por codigo + ENTER o lector de codigos de barras + ENTER excluyendo ya cargados
            elif action == 'get_producto':
                ids_exclude = json.loads(request.POST['excluir'])
                term = request.POST['term'].strip()
                try:
                    producto = Productos.objects.get(
                        Q(codigo__icontains=term) | Q(codigoProveedor__icontains=term)
                        | Q(codigoBarras1__icontains=term))
                    if producto.id not in ids_exclude:
                        item = producto.toJSON()
                        data['producto'] = item
                    else:
                        data['error'] = 'El Producto ya se encuentra en el listado'
                except Exception as e:
                    data['error'] = str(e)
            # Buscamos todos los productos excluyendo ya cargados
            elif action == 'search_all_productos':
                data = []
                ids_exclude = json.loads(request.POST['excluir'])
                for i in Productos.objects.all().exclude(id__in=ids_exclude):
                    data.append(i.toJSON())
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

