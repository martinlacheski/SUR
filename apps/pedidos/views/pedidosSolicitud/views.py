from django.contrib.sites.shortcuts import get_current_site
import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.erp.forms import ProductosForm
from apps.erp.models import Productos, Categorias, Subcategorias
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import Empresa, TiposIVA
from apps.pedidos.createSolicitudes import crearSolicitudes
from apps.pedidos.forms import PedidosSolicitudForm
from apps.pedidos.models import PedidosSolicitud, DetallePedidoSolicitud
from config import settings

from weasyprint import HTML, CSS


class PedidosSolicitudListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = PedidosSolicitud
    template_name = 'pedidosSolicitud/list.html'
    permission_required = 'pedidos.view_pedidossolicitud'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in PedidosSolicitud.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetallePedidoSolicitud.objects.filter(pedido_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Solicitudes de Pedidos'
        context['create_url'] = reverse_lazy('pedidos:pedidos_solicitudes_create')
        context['list_url'] = reverse_lazy('pedidos:pedidos_solicitudes_list')
        context['entity'] = 'Solicitudes de Pedidos'
        return context


class PedidosSolicitudCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = PedidosSolicitud
    form_class = PedidosSolicitudForm
    template_name = 'pedidosSolicitud/create.html'
    success_url = reverse_lazy('pedidos:pedidos_solicitudes_list')
    permission_required = 'pedidos.add_pedidossolicitud'
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
            # Generamos el Codigo para el nuevo producto
            elif action == 'generar_codigo_producto':
                ultimo_prod = Productos.objects.all().order_by('-id')[0]
                nuevo_cod = str(ultimo_prod.id + 1)
                if ultimo_prod.id <= 99999:
                    while len(nuevo_cod) <= 4:
                        nuevo_cod = '0' + nuevo_cod
                data['codigo'] = nuevo_cod
            # Generamos el Codigo para el nuevo producto
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
                    # obtenemos el Usuario actual
                    pedido.usuario = request.user
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
        context['title'] = 'Crear Solicitud de Pedido'
        context['entity'] = 'Solicitudes de Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['categorias'] = Categorias.objects.all()
        context['formProducto'] = ProductosForm()
        return context


class PedidosSolicitudUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PedidosSolicitud
    form_class = PedidosSolicitudForm
    template_name = 'pedidosSolicitud/create.html'
    success_url = reverse_lazy('pedidos:pedidos_solicitudes_list')
    permission_required = 'pedidos.change_pedidossolicitud'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PedidosSolicitudForm(instance=instance)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # Buscamos los distintos productos ingresando por teclado excluyendo ya cargados
            if action == 'search_productos':
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
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetallePedidoSolicitud.objects.filter(pedido_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['costo'] = i.costo
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
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
            elif action == 'edit':
                with transaction.atomic():
                    formPedidoRequest = json.loads(request.POST['pedido'])
                    # Obtenemos la Solicitud de Pedido que se esta editando
                    pedido = self.get_object()
                    # obtenemos el Usuario actual
                    pedido.usuario = request.user
                    pedido.fecha = formPedidoRequest['fecha']
                    pedido.fechaLimite = formPedidoRequest['fechaLimite']
                    pedido.subtotal = float(formPedidoRequest['subtotal'])
                    pedido.iva = float(formPedidoRequest['iva'])
                    pedido.total = float(formPedidoRequest['total'])
                    pedido.save()
                    # Eliminamos todos los productos del Detalle
                    pedido.detallepedidosolicitud_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPedidoRequest['productos']:
                        det = DetallePedidoSolicitud()
                        det.pedido_id = pedido.id
                        try:
                            det.proveedor_id = i['proveedor']
                        except:
                            pass
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.costo = float(i['costo'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Devolvemos en Data la ID de la Solicitud de Pedido para poder generar la Boleta
                    data = {'id': pedido.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Solicitud de Pedido'
        context['entity'] = 'Solicitudes de Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['categorias'] = Categorias.objects.all()
        context['formProducto'] = ProductosForm()
        return context


class PedidosSolicitudConfirmView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PedidosSolicitud
    form_class = PedidosSolicitudForm
    template_name = 'pedidosSolicitud/create.html'
    success_url = reverse_lazy('pedidos:pedidos_solicitudes_list')
    permission_required = 'pedidos.change_pedidossolicitud'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PedidosSolicitudForm(instance=instance)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        dominio = ''.join(['http://', get_current_site(request).domain])
        try:
            action = request.POST['action']
            # Buscamos los distintos productos ingresando por teclado excluyendo ya cargados
            if action == 'search_productos':
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
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetallePedidoSolicitud.objects.filter(pedido_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['costo'] = i.costo
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
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
            elif action == 'confirm':
                #Acá hay que ver (confirm)
                with transaction.atomic():
                    formPedidoRequest = json.loads(request.POST['pedido'])
                    # Obtenemos la Solicitud de Pedido que se esta editando
                    pedido = self.get_object()
                    # obtenemos el Usuario actual
                    pedido.usuario = request.user
                    # print(reverse_lazy('pedidos:pedidos_solicitudes_update') + '/' + str(pedido.id) + '/')
                    pedido.fecha = formPedidoRequest['fecha']
                    pedido.fechaLimite = formPedidoRequest['fechaLimite']
                    pedido.subtotal = float(formPedidoRequest['subtotal'])
                    pedido.iva = float(formPedidoRequest['iva'])
                    pedido.total = float(formPedidoRequest['total'])
                    pedido.estado = True
                    pedido.save()
                    # Eliminamos todos los productos del Detalle
                    pedido.detallepedidosolicitud_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPedidoRequest['productos']:
                        det = DetallePedidoSolicitud()
                        det.pedido_id = pedido.id
                        try:
                            det.proveedor_id = i['proveedor']
                        except:
                            pass
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.costo = float(i['costo'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Devolvemos en Data la ID de la Solicitud de Pedido para poder generar la Boleta
                    data = {'id': pedido.id}
                    data['redirect'] = self.url_redirect
                    crearSolicitudes(pedido, dominio) # Arma link y prepara solicitud para proveedor
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Confirmar Solicitud de Pedido'
        context['entity'] = 'Solicitudes de Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'confirm'
        context['categorias'] = Categorias.objects.all()
        context['formProducto'] = ProductosForm()
        return context


class PedidosSolicitudDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PedidosSolicitud
    form_class = PedidosSolicitudForm
    template_name = 'pedidosSolicitud/create.html'
    success_url = reverse_lazy('pedidos:pedidos_solicitudes_list')
    permission_required = 'pedidos.delete_pedidossolicitud'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                with transaction.atomic():
                    # Obtenemos la solicitud de pedido que se esta editando
                    pedido = self.get_object()
                    # obtenemos el Usuario actual
                    pedido.usuario = request.user
                    # Eliminamos la Solicitud de Pedido
                    pedido.estado = False
                    pedido.save()
                    data['redirect'] = self.url_redirect
                    data['check'] = 'ok'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancelar Solicitud de Pedido'
        context['entity'] = 'Solicitudes de Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class PedidosSolicitudPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'pedidos.view_pedidossolicitud'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Utilizamos el template para generar el PDF
            template = get_template('pedidosSolicitud/pdf.html')
            context = {
                'pedido': PedidosSolicitud.objects.get(pk=self.kwargs['pk']),
                'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                            'localidad': empresa.localidad.get_full_name(), 'imagen': empresa.imagen},
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
        return HttpResponseRedirect(reverse_lazy('pedidos:pedidos_solicitudes_list'))
