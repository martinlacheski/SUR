import datetime
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

from apps.erp.forms import VentasForm, ClientesForm, ServiciosForm, ProductosForm
from apps.erp.models import Ventas, Productos, Servicios, DetalleProductosVenta, DetalleServiciosVenta, Clientes, \
    Categorias, Subcategorias
from apps.mixins import ValidatePermissionRequiredMixin
from apps.numlet import NumeroALetras
from apps.parametros.models import Empresa, TiposIVA
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
                for i in Ventas.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detalle_servicios':
                data = []
                for i in DetalleServiciosVenta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            # Buscamos si la venta tiene TRABAJO
            elif action == 'search_TrabajoID':
                venta = Ventas.objects.get(id=request.POST['pk'])
                data['trabajoID'] = venta.trabajo
            elif action == 'create_reporte':
                # Traemos la empresa para obtener los valores
                empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
                # Utilizamos el template para generar el PDF
                template = get_template('ventas/report.html')
                # Obtenemos el detalle del Reporte
                reporte = json.loads(request.POST['reporte'])
                # Obtenemos el Cliente si esta filtrado
                cliente = ""
                try:
                    cliente = reporte['cliente']
                except Exception as e:
                    pass
                # Obtenemos si se filtro por rango de fechas
                inicio = ""
                fin = ""
                try:
                    inicio = reporte['fechaDesde']
                    fin = reporte['fechaHasta']
                except Exception as e:
                    pass
                # Obtenemos si se quito las Canceladas
                soloTrabajos = False
                try:
                    soloTrabajos = reporte['excluirSinTrabajos']
                except Exception as e:
                    pass
                # Obtenemos si se quito las Canceladas
                canceladas = False
                try:
                    canceladas = reporte['excluirCanceladas']
                except Exception as e:
                    pass
                # Obtenemos las ventas
                ventas = []
                try:
                    ventas = reporte['ventas']
                    for venta in ventas:
                        venta['subtotal'] = float(venta['subtotal'])
                        venta['iva'] = float(venta['iva'])
                        venta['percepcion'] = float(venta['percepcion'])
                        venta['total'] = float(venta['total'])
                except Exception as e:
                    pass
                total = 0
                neto = 0
                iva = 0
                percepcion = 0
                try:
                    for i in ventas:
                        if i['estadoVenta']:
                            neto += float(i['subtotal'])
                            iva += float(i['iva'])
                            percepcion += float(i['percepcion'])
                            total += float(i['total'])
                    neto = round(neto, 2)
                    iva = round(iva, 2)
                    percepcion = round(percepcion, 2)
                    total = round(total, 2)
                except Exception as e:
                    pass
                # Pasamos a letras el total
                totalEnLetras = NumeroALetras(total).a_letras.upper()
                #   cargamos los datos del contexto
                try:
                    context = {
                        'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                                    'localidad': empresa.localidad.get_full_name(), 'imagen': empresa.imagen},
                        'fecha': datetime.datetime.now(),
                        'cliente': cliente,
                        'inicio': inicio,
                        'fin': fin,
                        'canceladas': canceladas,
                        'soloTrabajos': soloTrabajos,
                        'ventas': ventas,
                        'usuario': request.user,
                        'subtotal': neto,
                        'iva': iva,
                        'percepcion': percepcion,
                        'total': total,
                        'enLetras': totalEnLetras,
                    }
                    # Generamos el render del contexto
                    html = template.render(context)
                    # Asignamos la ruta donde se guarda el PDF
                    urlWrite = settings.MEDIA_ROOT + 'reportes/reporteVentas.pdf'
                    # Asignamos la ruta donde se visualiza el PDF
                    urlReporte = settings.MEDIA_URL + 'reportes/reporteVentas.pdf'
                    # Asignamos la ruta del CSS de BOOTSTRAP
                    css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
                    # Creamos el PDF
                    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)],
                                                                                             target=urlWrite)
                    data['url'] = urlReporte
                except Exception as e:
                    data['error'] = str(e)
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


class VentasAuditListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Productos
    template_name = 'ventas/audit.html'
    permission_required = 'erp.view_ventas'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Ventas.history.all():
                    try:
                        usuario = i.history_user.username
                    except:
                        usuario = '----'
                    dict = {'history_id': i.history_id, 'fecha': i.fecha, 'venta_id': i.id,
                            'cliente': i.cliente.razonSocial, 'condicionVenta': i.condicionVenta.nombre,
                            'medioPago': i.medioPago.nombre, 'trabajo': i.trabajo,
                            'subtotal': i.subtotal, 'iva': i.iva, 'percepcion': i.percepcion, 'total': i.total,
                            'usuario': i.usuario.username, 'estadoVenta': i.estadoVenta,
                            'history_date': i.history_date, 'history_type': i.history_type, 'history_user': usuario}
                    data.append(dict)
            elif action == 'view_movimiento':
                data = []
                mov = Ventas.history.get(history_id=request.POST['pk'])
                movAnt = mov.prev_record
                try:
                    usuario = mov.history_user.username
                    movAnt = mov.prev_record
                except:
                    usuario = '----'
                if movAnt:
                    dict = {'usuario': mov.usuario.username, 'fecha': mov.fecha, 'venta_id': mov.id,
                            'cliente': mov.cliente.razonSocial, 'condicionVenta': mov.condicionVenta.nombre,
                            'medioPago': mov.medioPago.nombre, 'trabajo': mov.trabajo,
                            'subtotal': mov.subtotal, 'iva': mov.iva, 'percepcion': mov.percepcion, 'total': mov.total,
                            'estadoVenta': mov.estadoVenta,
                            'history_date': mov.history_date, 'history_type': mov.history_type, 'history_user': usuario,
                            'usuarioOld': movAnt.usuario.username, 'fechaOld': movAnt.fecha,
                            'clienteOld': movAnt.cliente.razonSocial, 'condicionVentaOld': movAnt.condicionVenta.nombre,
                            'medioPagoOld': movAnt.medioPago.nombre, 'trabajoOld': movAnt.trabajo,
                            'subtotalOld': movAnt.subtotal, 'ivaOld': movAnt.iva, 'percepcionOld': movAnt.percepcion,
                            'totalOld': movAnt.total, 'estadoVentaOld': movAnt.estadoVenta,
                            'history_dateOld': movAnt.history_date, 'history_typeOld': movAnt.history_type}
                    item = dict
                else:
                    dict = {'usuario': mov.usuario.username, 'fecha': mov.fecha, 'venta_id': mov.id,
                            'cliente': mov.cliente.razonSocial, 'condicionVenta': mov.condicionVenta.nombre,
                            'medioPago': mov.medioPago.nombre, 'trabajo': mov.trabajo,
                            'subtotal': mov.subtotal, 'iva': mov.iva, 'percepcion': mov.percepcion, 'total': mov.total,
                            'estadoVenta': mov.estadoVenta}
                    item = dict
                # Obtenemos el ID de la venta para Filtrar
                venta = request.POST['venta_id']
                # Creamos unas variables para realizar los filtros
                # detalle_productos = []
                # ids_exclude= []
                # Obtenemos los detalles que corresponden a la venta
                # ventaFiltrar = DetalleProductosVenta.history.filter(venta_id=venta)
                # for i in ventaFiltrar:
                #     if i.producto.id not in ids_exclude:
                #         detalle = {
                #             'producto': i.producto.descripcion, 'precio': i.precio, 'cantidad': i.cantidad,
                #             'subtotal': i.subtotal, 'history_type': i.history_type, 'history_id': i.history_id}
                #         detalle_productos.append(detalle)
                #         ids_exclude.append(i.producto.id)
                # for prod in ids_exclude:
                #     val = ventaFiltrar.filter(producto_id=prod)
                #     last = val.order_by("-id")[0]
                #     print(last.history_id)
                detalle_productos = []
                for i in DetalleProductosVenta.history.filter(venta_id=venta).order_by('producto__descripcion'):
                    # i = i.next_record
                    detalle = {
                        'producto': i.producto.descripcion, 'precio': i.precio, 'cantidad': i.cantidad,
                        'subtotal': i.subtotal, 'history_type': i.history_type, 'history_id': i.history_id}
                    detalle_productos.append(detalle)
                item['detalle_productos'] = detalle_productos
                detalle_servicios = []
                for i in DetalleServiciosVenta.history.filter(venta_id=venta).order_by('servicio__descripcion'):
                    # i = i.next_record
                    detalle = {
                        'servicio': i.servicio.descripcion, 'precio': i.precio, 'cantidad': i.cantidad,
                        'subtotal': i.subtotal, 'history_type': i.history_type, 'history_id': i.history_id}
                    detalle_servicios.append(detalle)
                item['detalle_servicios'] = detalle_servicios
                data.append(item)
            elif action == 'create_reporte':
                # Traemos la empresa para obtener los valores
                empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
                # Utilizamos el template para generar el PDF
                template = get_template('ventas/reportAuditoria.html')
                # Obtenemos el detalle del Reporte
                reporte = json.loads(request.POST['reporte'])
                # Obtenemos el producto si esta filtrado
                venta = ""
                try:
                    venta = reporte['venta']
                except Exception as e:
                    pass
                # Obtenemos el usuario si esta filtrado
                usuario = ""
                try:
                    usuario = reporte['usuario']
                except Exception as e:
                    pass
                # Obtenemos la accion si esta filtrada
                accion = ""
                try:
                    accion = reporte['accion']
                except Exception as e:
                    pass
                # Obtenemos si se filtro por rango de fechas
                inicio = ""
                fin = ""
                try:
                    inicio = reporte['fechaDesde']
                    fin = reporte['fechaHasta']
                except Exception as e:
                    pass
                # Obtenemos el reporte
                ventas = []
                try:
                    ventas = reporte['ventas']
                    for vent in ventas:
                        vent['subtotal'] = float(vent['subtotal'])
                        vent['iva'] = float(vent['iva'])
                        vent['percepcion'] = float(vent['percepcion'])
                        vent['total'] = float(vent['total'])
                except Exception as e:
                    pass
                #   cargamos los datos del contexto
                try:
                    context = {
                        'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                                    'localidad': empresa.localidad.get_full_name(), 'imagen': empresa.imagen},
                        'fecha': datetime.datetime.now(),
                        'venta': venta,
                        'accion': accion,
                        'inicio': inicio,
                        'fin': fin,
                        'ventas': ventas,
                        'usuarioAuditoria': usuario,
                        'usuario': request.user,
                    }
                    # Generamos el render del contexto
                    html = template.render(context)
                    # Asignamos la ruta donde se guarda el PDF
                    urlWrite = settings.MEDIA_ROOT + 'reportes/reporteAuditoriaVentas.pdf'
                    # Asignamos la ruta donde se visualiza el PDF
                    urlReporte = settings.MEDIA_URL + 'reportes/reporteAuditoriaVentas.pdf'
                    # Asignamos la ruta del CSS de BOOTSTRAP
                    css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
                    # Creamos el PDF
                    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)],
                                                                                             target=urlWrite)
                    data['url'] = urlReporte
                except Exception as e:
                    data['error'] = str(e)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Auditoría de Ventas'
        context['list_url'] = reverse_lazy('erp:ventas_audit')
        context['entity'] = 'Auditoría Ventas'
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
                    | Q(codigoBarras1__icontains=term))[0:10]
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
            # Buscamos todos los productos
            elif action == 'search_all_productos':
                data = []
                for i in Productos.objects.all():
                    data.append(i.toJSON())
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
            # Buscamos todos los Servicios
            elif action == 'search_all_servicios':
                data = []
                for i in Servicios.objects.all():
                    data.append(i.toJSON())
            # Buscamos el IVA para el MODAL de Productos y Servicios
            elif action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            # si no existe el Producto lo creamos
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # Select Anidado de Categorias
            elif action == 'search_subcategorias':
                data = [{'id': '', 'text': '---------'}]
                for i in Subcategorias.objects.filter(categoria_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            # si no existe el Servicio lo creamos
            elif action == 'create_servicio':
                with transaction.atomic():
                    formServicio = ServiciosForm(request.POST)
                    data = formServicio.save()
            # Actualizacion de Precio PRODUCTO
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
                data['costo'] = producto.costo
                data['precioVenta'] = producto.precioVenta
            # Actualizacion de Precio SERVICIO
            elif action == 'update_precioServicio':
                with transaction.atomic():
                    servicio = Servicios.objects.get(id=request.POST['pk'])
                    servicio.costo = float(request.POST['costo'])
                    servicio.precioVenta = float(request.POST['precioVenta'])
                    servicio.save()
            # Buscamos el Precio del Servicio luego de actualizar el precio
            elif action == 'search_precioServicio':
                servicio = Servicios.objects.get(id=request.POST['pk'])
                data['costo'] = servicio.costo
                data['precioVenta'] = servicio.precioVenta
            elif action == 'add':
                with transaction.atomic():
                    formVentaRequest = json.loads(request.POST['venta'])
                    venta = Ventas()
                    venta.fecha = formVentaRequest['fecha']
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
                        if det.producto.descuentaStock == True:
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
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['categorias'] = Categorias.objects.all()
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
        # Obtenemos unicamente el CLIENTE en el que se CREO la VENTA, para poder modificar la misma
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
                    | Q(codigoBarras1__icontains=term))[0:10]
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
            # Buscamos todos los productos
            elif action == 'search_all_productos':
                data = []
                for i in Productos.objects.all():
                    data.append(i.toJSON())
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
            # Buscamos todos los Servicios
            elif action == 'search_all_servicios':
                data = []
                for i in Servicios.objects.all():
                    data.append(i.toJSON())
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
            # Buscamos el IVA para el MODAL de Productos y Servicios
            elif action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            # si no existe el Producto lo creamos
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # Select Anidado de Categorias
            elif action == 'search_subcategorias':
                data = [{'id': '', 'text': '---------'}]
                for i in Subcategorias.objects.filter(categoria_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            # si no existe el Servicio lo creamos
            elif action == 'create_servicio':
                with transaction.atomic():
                    formServicio = ServiciosForm(request.POST)
                    data = formServicio.save()
            # Actualizacion de Precio PRODUCTO
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
                data['costo'] = producto.costo
                data['precioVenta'] = producto.precioVenta
            # Actualizacion de Precio SERVICIO
            elif action == 'update_precioServicio':
                with transaction.atomic():
                    servicio = Servicios.objects.get(id=request.POST['pk'])
                    servicio.costo = float(request.POST['costo'])
                    servicio.precioVenta = float(request.POST['precioVenta'])
                    servicio.save()
            # Buscamos el Precio del Servicio luego de actualizar el precio
            elif action == 'search_precioServicio':
                servicio = Servicios.objects.get(id=request.POST['pk'])
                data['costo'] = servicio.costo
                data['precioVenta'] = servicio.precioVenta
            elif action == 'edit':
                with transaction.atomic():
                    formVentaRequest = json.loads(request.POST['venta'])
                    # Obtenemos la venta que se esta editando
                    venta = self.get_object()
                    venta.fecha = formVentaRequest['fecha']
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
                        if prod.producto.descuentaStock == True:
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
                        if det.producto.descuentaStock == True:
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
        context['categorias'] = Categorias.objects.all()
        context['formCliente'] = ClientesForm()
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
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
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Utilizamos el template para generar el PDF
            template = get_template('ventas/pdf.html')
            # Obtenemos el subtotal de Productos y Servicios para visualizar en el template
            subtotalProductos = DetalleProductosVenta.objects.filter(venta_id=self.kwargs['pk'])
            subtotalServicios = DetalleServiciosVenta.objects.filter(venta_id=self.kwargs['pk'])
            productos = 0
            for i in subtotalProductos:
                productos += i.subtotal
            servicios = 0
            for i in subtotalServicios:
                servicios += i.subtotal
            # Obtenemos el valor total para pasar a letras
            total = Ventas.objects.get(pk=self.kwargs['pk']).total
            # Pasamos a letras el total
            totalEnLetras = NumeroALetras(total).a_letras.upper()
            # cargamos los datos del contexto
            context = {
                'venta': Ventas.objects.get(pk=self.kwargs['pk']),
                'enLetras': totalEnLetras,
                'subtotalProductos': productos,
                'subtotalServicios': servicios,
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
        return HttpResponseRedirect(reverse_lazy('erp:ventas_list'))
