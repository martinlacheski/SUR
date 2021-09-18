import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q, Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.erp.forms import VentasForm, ClientesForm
from apps.erp.models import Ventas, Productos, Servicios, DetalleProductosVenta, DetalleServiciosVenta, Clientes
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import Empresa
from config import settings

from weasyprint import HTML, CSS


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
                        # Descontamos el Stock de los productos
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
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosVenta.objects.filter(venta_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosVenta.objects.filter(venta_id=self.get_object().id):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'edit':
                with transaction.atomic():
                    formVentaRequest = json.loads(request.POST['venta'])
                    # Obtenemos la venta que se esta editando
                    venta = self.get_object()
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
                    # Reestablecemos el stock de los productos
                    for prod in DetalleProductosVenta.objects.filter(venta_id=self.get_object().id):
                        prod.producto.stockReal += prod.cantidad
                        prod.producto.save()
                    # Eliminamos todos los productos del Detalle
                    venta.detalleproductosventa_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formVentaRequest['productos']:
                        det = DetalleProductosVenta()
                        det.venta_id = venta.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Descontamos el Stock de los Productos del Detalle
                        det.producto.stockReal -= det.cantidad
                        det.producto.save()
                    # Eliminamos del detalle todos los Servicios del Detalle
                    venta.detalleserviciosventa_set.all().delete()
                    # Volvemos a cargar todos los Servicios del Detalle
                    for i in formVentaRequest['servicios']:
                        det = DetalleServiciosVenta()
                        det.venta_id = venta.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Devolvemos en Data la ID de la nueva Venta para poder generar la Boleta
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
        return context


class VentasDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('erp:ventas_list')
    permission_required = 'erp.delete_ventas'
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
                    # Obtenemos la venta que se esta editando
                    venta = self.get_object()
                    # Reestablecemos el stock de los productos
                    for prod in DetalleProductosVenta.objects.filter(venta_id=self.get_object().id):
                        prod.producto.stockReal += prod.cantidad
                        prod.producto.save()
                    # Eliminamos la venta
                    venta.estadoVenta = False
                    venta.save()
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
        context['title'] = 'Cancelar una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class VentasPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'erp.view_ventas'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(id=1)
            # Utilizamos el template para generar el PDF
            template = get_template('ventas/pdf.html')
            # template = get_template('ventas/invoice.html')
            # Obtenemos el subtotal de Productos y Servicios para visualizar en el template
            subtotalProductos = DetalleProductosVenta.objects.filter(venta_id=self.kwargs['pk'])
            subtotalServicios = DetalleServiciosVenta.objects.filter(venta_id=self.kwargs['pk'])
            productos = 0
            for i in subtotalProductos:
                productos += i.subtotal
            servicios = 0
            for i in subtotalServicios:
                servicios += i.subtotal
            # cargamos los datos del contexto
            context = {
                'venta': Ventas.objects.get(pk=self.kwargs['pk']),
                'subtotalProductos': productos,
                'subtotalServicios': servicios,
                'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                            'localidad': empresa.localidad.get_full_name(), 'imagen': empresa.imagen},

                # 'imagen': '{}{}'.format(settings.MEDIA_URL, empresa.get_imagen())
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
        return HttpResponseRedirect(reverse_lazy('erp:ventas_list'))