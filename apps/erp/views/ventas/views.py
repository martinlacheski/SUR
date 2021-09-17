import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.erp.forms import VentasForm, ClientesForm
from apps.erp.models import Ventas, Productos, Servicios, DetalleProductosVenta, DetalleServiciosVenta, Clientes
from apps.mixins import ValidatePermissionRequiredMixin


class VentasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Ventas
    template_name = 'ventas/list.html'
    permission_required = 'erp.view_ventas'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Ventas.objects.all()[0:15]:
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detalle_servicios':
                data = []
                for i in DetalleServiciosVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:ventas_create')
        context['list_url'] = reverse_lazy('erp:ventas_list')
        context['entity'] = 'Ventas'
        return context


class VentasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('erp:ventas_list')
    permission_required = 'erp.add_ventas'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # buscamos la percepcion del cliente
            if action == 'search_percepcion':
                cliente = Clientes.objects.get(id=request.POST['pk'])
                data['percepcion'] = cliente.tipoPercepcion.percepcion
            # si no existe el cliente lo creamos
            elif action == 'create_cliente':
                with transaction.atomic():
                    formCliente = ClientesForm(request.POST)
                    data = formCliente.save()
            # Buscamos los distintos productos ingresando por teclado
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
            # Metodo para obtener un producto por codigo + ENTER o lector de codigos de barras + ENTER
            elif action == 'get_producto':
                term = request.POST['term'].strip()
                try:
                    producto = Productos.objects.get(
                        Q(codigo__icontains=term) | Q(codigoProveedor__icontains=term)
                        | Q(codigoBarras1__icontains=term))
                    item = producto.toJSON()
                    data['producto'] = item
                except Exception as e:
                    data['error'] = str(e)
            # Buscamos los distintos servicios ingresando por teclado
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
            # Metodo para obtener un servicio por codigo + ENTER o lector de codigos de barras + ENTER
            elif action == 'get_servicio':
                term = request.POST['term'].strip()
                try:
                    servicio = Servicios.objects.get(Q(codigo__icontains=term))
                    item = servicio.toJSON()
                    data['servicio'] = item
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'add':
                with transaction.atomic():
                    formVentaRequest = json.loads(request.POST['venta'])
                    venta = Ventas()
                    venta.fecha = formVentaRequest['fecha']
                    venta.tipoComprobante_id = formVentaRequest['tipoComprobante']
                    # obtenemos el Usuario actual
                    venta.usuario = request.user
                    venta.cliente_id = formVentaRequest['cliente']
                    venta.condicionVenta_id = formVentaRequest['condicionVenta']
                    venta.medioPago_id = formVentaRequest['medioPago']
                    venta.subtotal = float(formVentaRequest['subtotal'])
                    venta.iva = float(formVentaRequest['iva'])
                    venta.percepcion = float(formVentaRequest['percepcion'])
                    venta.total = float(formVentaRequest['total'])
                    venta.save()
                    for i in formVentaRequest['productos']:
                        det = DetalleProductosVenta()
                        det.venta_id = venta.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.producto.stockReal -= det.cantidad
                        det.producto.save()
                    for i in formVentaRequest['servicios']:
                        det = DetalleServiciosVenta()
                        det.venta_id = venta.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': venta.id}
                    data['redirect'] = self.url_redirect
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
        context['formCliente'] = ClientesForm()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context


class VentasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('erp:ventas_list')
    permission_required = 'erp.change_ventas'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = VentasForm(instance=instance)
        form.fields['cliente'].queryset = Clientes.objects.filter(id=instance.cliente.id)
        return form

    def get_detalle_productos(self):
        data = []
        try:
            for i in DetalleProductosVenta.objects.filter(venta_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                data.append(item)
        except:
            pass
        return data

    def get_detalle_servicios(self):
        data = []
        try:
            for i in DetalleServiciosVenta.objects.filter(venta_id=self.get_object().id):
                item = i.servicio.toJSON()
                item['cantidad'] = i.cantidad
                data.append(item)
        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # buscamos la percepcion del cliente
            if action == 'search_percepcion':
                cliente = Clientes.objects.get(id=request.POST['pk'])
                data['percepcion'] = cliente.tipoPercepcion.percepcion
            # si no existe el cliente lo creamos
            elif action == 'create_cliente':
                with transaction.atomic():
                    formCliente = ClientesForm(request.POST)
                    data = formCliente.save()
            # Buscamos los distintos productos ingresando por teclado
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
            # Metodo para obtener un producto por codigo + ENTER o lector de codigos de barras + ENTER
            elif action == 'get_producto':
                term = request.POST['term'].strip()
                try:
                    producto = Productos.objects.get(
                        Q(codigo__icontains=term) | Q(codigoProveedor__icontains=term)
                        | Q(codigoBarras1__icontains=term))
                    item = producto.toJSON()
                    data['producto'] = item
                except Exception as e:
                    data['error'] = str(e)
            # Buscamos los distintos servicios ingresando por teclado
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
            # Metodo para obtener un servicio por codigo + ENTER o lector de codigos de barras + ENTER
            elif action == 'get_servicio':
                term = request.POST['term'].strip()
                try:
                    servicio = Servicios.objects.get(Q(codigo__icontains=term))
                    item = servicio.toJSON()
                    data['servicio'] = item
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'edit':
                with transaction.atomic():
                    formVentaRequest = json.loads(request.POST['venta'])
                    venta = Ventas()
                    venta.fecha = formVentaRequest['fecha']
                    venta.tipoComprobante_id = formVentaRequest['tipoComprobante']
                    # obtenemos el Usuario actual
                    venta.usuario = request.user
                    venta.cliente_id = formVentaRequest['cliente']
                    venta.condicionVenta_id = formVentaRequest['condicionVenta']
                    venta.medioPago_id = formVentaRequest['medioPago']
                    venta.subtotal = float(formVentaRequest['subtotal'])
                    venta.iva = float(formVentaRequest['iva'])
                    venta.percepcion = float(formVentaRequest['percepcion'])
                    venta.total = float(formVentaRequest['total'])
                    venta.save()
                    for i in formVentaRequest['productos']:
                        det = DetalleProductosVenta()
                        det.venta_id = venta.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.producto.stockReal -= det.cantidad
                        det.producto.save()
                    for i in formVentaRequest['servicios']:
                        det = DetalleServiciosVenta()
                        det.venta_id = venta.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': venta.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['formCliente'] = ClientesForm()
        context['detalleProductos'] = self.get_detalle_productos()
        context['detalleServicios'] = self.get_detalle_servicios()
        return context