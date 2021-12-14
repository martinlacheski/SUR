import datetime
import json
import os
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.erp.forms import ProductosForm, ServiciosForm, ClientesForm
from apps.erp.models import Productos, Servicios, Clientes, Categorias, Subcategorias
from apps.erp.views.compras.views import ComprasCreateView
from apps.mixins import ValidatePermissionRequiredMixin
from apps.numlet import NumeroALetras
from apps.parametros.forms import MarcasForm, ModelosForm
from apps.parametros.models import Modelos, Empresa, Marcas, TiposIVA, EstadoParametros, Prioridades
from apps.presupuestos.forms import PresupuestosForm
from apps.presupuestos.models import Presupuestos, DetalleProductosPresupuesto, DetalleServiciosPresupuesto, \
    PlantillaPresupuestos, DetalleProductosPlantillaPresupuesto, DetalleServiciosPlantillaPresupuesto
from apps.trabajos.models import Trabajos, DetalleProductosTrabajo, DetalleServiciosTrabajo
from apps.usuarios.models import Usuarios
from config import settings

from weasyprint import HTML, CSS


class PresupuestosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Presupuestos
    template_name = 'presupuestos/list.html'
    permission_required = 'presupuestos.view_presupuestos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Presupuestos.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosPresupuesto.objects.filter(presupuesto_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detalle_servicios':
                data = []
                for i in DetalleServiciosPresupuesto.objects.filter(presupuesto_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'create_reporte':
                # Traemos la empresa para obtener los valores
                empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
                # Armamos el Logo de la Empresa
                logo = "file://" + str(settings.MEDIA_ROOT) + str(empresa.imagen)
                # Utilizamos el template para generar el PDF
                template = get_template('presupuestos/report.html')
                # Obtenemos el detalle del Reporte
                reporte = json.loads(request.POST['reporte'])
                # Obtenemos el Cliente si esta filtrado
                cliente = ""
                try:
                    cliente = reporte['cliente']
                except Exception as e:
                    pass
                # Obtenemos el Modelo si esta filtrado
                modelo = ""
                try:
                    modelo = reporte['modelo']
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
                soloConfirmados = False
                try:
                    soloConfirmados = reporte['excluirNoConfirmados']
                except Exception as e:
                    pass
                # Obtenemos si se quito las Canceladas
                cancelados = False
                try:
                    cancelados = reporte['excluirCancelados']
                except Exception as e:
                    pass
                # Obtenemos los presupuestos
                presupuestos = []
                try:
                    presupuestos = reporte['presupuestos']
                    for presupuesto in presupuestos:
                        presupuesto['total'] = float(presupuesto['total'])
                except Exception as e:
                    pass
                total = 0
                neto = 0
                iva = 0
                percepcion = 0
                try:
                    for i in presupuestos:
                        if i['estado']:
                            neto += float(i['subtotal'])
                            iva += float(i['iva'])
                            percepcion += float(i['percepcion'])
                            total += float(i['total'])
                    neto = round(neto, 2)
                    iva = round(iva, 2)
                    percepcion = round(percepcion, 2)
                    total = round(total, 2)
                except Exception as e:
                    print(str(e))
                    pass
                # Pasamos a letras el total
                totalEnLetras = NumeroALetras(total).a_letras.upper()
                #   cargamos los datos del contexto
                try:
                    context = {
                        'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                                    'localidad': empresa.localidad.get_full_name(), 'imagen': logo},
                        'fecha': datetime.datetime.now(),
                        'cliente': cliente,
                        'modelo': modelo,
                        'inicio': inicio,
                        'fin': fin,
                        'cancelados': cancelados,
                        'soloConfirmados': soloConfirmados,
                        'presupuestos': presupuestos,
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
                    urlWrite = settings.MEDIA_ROOT + 'reportePresupuestos.pdf'
                    # Asignamos la ruta donde se visualiza el PDF
                    urlReporte = settings.MEDIA_URL + 'reportePresupuestos.pdf'
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
        context['title'] = 'Listado de Presupuestos'
        context['create_url'] = reverse_lazy('presupuestos:presupuestos_create')
        context['list_url'] = reverse_lazy('presupuestos:presupuestos_list')
        context['entity'] = 'Presupuestos'
        return context


class PresupuestosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Presupuestos
    form_class = PresupuestosForm
    template_name = 'presupuestos/create.html'
    success_url = reverse_lazy('presupuestos:presupuestos_list')
    permission_required = 'presupuestos.add_presupuestos'
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
            # si no existe la marca la creamos
            elif action == 'create_marca':
                with transaction.atomic():
                    formMarca = MarcasForm(request.POST)
                    data = formMarca.save()
            # si no existe el modelo lo creamos
            elif action == 'create_modelo':
                with transaction.atomic():
                    formModelo = ModelosForm(request.POST)
                    data = formModelo.save()
            elif action == 'search_modelos':
                data = [{'id': '', 'text': '---------'}]
                for i in Modelos.objects.filter(marca_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            # Buscamos las plantillas de Presupuestos creadas
            elif action == 'search_plantillas':
                data = [{'id': '', 'text': '---------'}]
                for i in PlantillaPresupuestos.objects.filter(modelo_id=request.POST['pk']).exclude(estado=False):
                    data.append({'id': i.id, 'text': i.get_full_name()})
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosPlantillaPresupuesto.objects.filter(
                            presupuestoPlantilla_id=request.POST['pk']):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.producto.precioVenta
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosPlantillaPresupuesto.objects.filter(
                            presupuestoPlantilla_id=request.POST['pk']):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.servicio.precioVenta
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
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
            # Guardamos el Producto creado
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # Generamos el Codigo para el nuevo Servicio
            elif action == 'generar_codigo_servicio':
                ultimo_serv = Servicios.objects.all().order_by('-id')[0]
                nuevo_cod = str(ultimo_serv.id + 1)
                if ultimo_serv.id <= 99999:
                    while len(nuevo_cod) <= 4:
                        nuevo_cod = '0' + nuevo_cod
                data['codigo'] = nuevo_cod
            # Guardamos el Servicio creado
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
                    formPresupuestoRequest = json.loads(request.POST['presupuesto'])
                    presupuesto = Presupuestos()
                    presupuesto.fecha = formPresupuestoRequest['fecha']
                    # obtenemos el Usuario actual
                    presupuesto.usuario = request.user
                    presupuesto.cliente_id = formPresupuestoRequest['cliente']
                    presupuesto.validez = formPresupuestoRequest['validez']
                    presupuesto.modelo_id = formPresupuestoRequest['modelo']
                    presupuesto.subtotal = float(formPresupuestoRequest['subtotal'])
                    presupuesto.iva = float(formPresupuestoRequest['iva'])
                    presupuesto.percepcion = float(formPresupuestoRequest['percepcion'])
                    presupuesto.total = float(formPresupuestoRequest['total'])
                    presupuesto.observaciones = formPresupuestoRequest['observaciones']
                    presupuesto.save()
                    for i in formPresupuestoRequest['productos']:
                        det = DetalleProductosPresupuesto()
                        det.presupuesto_id = presupuesto.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    for i in formPresupuestoRequest['servicios']:
                        det = DetalleServiciosPresupuesto()
                        det.presupuesto_id = presupuesto.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': presupuesto.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['formCliente'] = ClientesForm()
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['presupuestosPlantilla'] = PlantillaPresupuestos.objects.all()
        context['categorias'] = Categorias.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context


class PresupuestosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Presupuestos
    form_class = PresupuestosForm
    template_name = 'presupuestos/create.html'
    success_url = reverse_lazy('presupuestos:presupuestos_list')
    permission_required = 'presupuestos.change_presupuestos'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PresupuestosForm(instance=instance)
        # Obtenemos unicamente el MODELO y CLIENTE en el que se CREO el PRESUPUESTO, para poder modificar la misma
        form.fields['modelo'].queryset = Modelos.objects.filter(id=instance.modelo.id)
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
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosPresupuesto.objects.filter(presupuesto_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosPresupuesto.objects.filter(presupuesto_id=self.get_object().id):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
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
            # Guardamos el Producto creado
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # Generamos el Codigo para el nuevo Servicio
            elif action == 'generar_codigo_servicio':
                ultimo_serv = Servicios.objects.all().order_by('-id')[0]
                nuevo_cod = str(ultimo_serv.id + 1)
                if ultimo_serv.id <= 99999:
                    while len(nuevo_cod) <= 4:
                        nuevo_cod = '0' + nuevo_cod
                data['codigo'] = nuevo_cod
            # Guardamos el Servicio creado
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
                    formPresupuestoRequest = json.loads(request.POST['presupuesto'])
                    # Obtenemos el Presupuesto Base que se esta editando
                    presupuesto = self.get_object()
                    presupuesto.fecha = formPresupuestoRequest['fecha']
                    # obtenemos el Usuario actual
                    presupuesto.usuario = request.user
                    presupuesto.cliente_id = formPresupuestoRequest['cliente']
                    presupuesto.modelo_id = formPresupuestoRequest['modelo']
                    presupuesto.subtotal = float(formPresupuestoRequest['subtotal'])
                    presupuesto.iva = float(formPresupuestoRequest['iva'])
                    presupuesto.percepcion = float(formPresupuestoRequest['percepcion'])
                    presupuesto.total = float(formPresupuestoRequest['total'])
                    presupuesto.observaciones = formPresupuestoRequest['observaciones']
                    presupuesto.save()
                    # Eliminamos todos los productos del Detalle
                    presupuesto.detalleproductospresupuesto_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoRequest['productos']:
                        det = DetalleProductosPresupuesto()
                        det.presupuesto_id = presupuesto.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Eliminamos todos los productos del Detalle
                    presupuesto.detalleserviciospresupuesto_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoRequest['servicios']:
                        det = DetalleServiciosPresupuesto()
                        det.presupuesto_id = presupuesto.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Devolvemos en Data la ID del Presupuesto Base para poder generar la Boleta
                    data = {'id': presupuesto.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['categorias'] = Categorias.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context


class PresupuestosConfirmView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Presupuestos
    form_class = PresupuestosForm
    template_name = 'presupuestos/create.html'
    success_url = reverse_lazy('presupuestos:presupuestos_list')
    permission_required = 'presupuestos.change_presupuestos'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PresupuestosForm(instance=instance)
        # Obtenemos unicamente el MODELO y CLIENTE en el que se CREO el PRESUPUESTO, para poder modificar la misma
        form.fields['modelo'].queryset = Modelos.objects.filter(id=instance.modelo.id)
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
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosPresupuesto.objects.filter(presupuesto_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosPresupuesto.objects.filter(presupuesto_id=self.get_object().id):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
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
            # Guardamos el Producto creado
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # Generamos el Codigo para el nuevo Servicio
            elif action == 'generar_codigo_servicio':
                ultimo_serv = Servicios.objects.all().order_by('-id')[0]
                nuevo_cod = str(ultimo_serv.id + 1)
                if ultimo_serv.id <= 99999:
                    while len(nuevo_cod) <= 4:
                        nuevo_cod = '0' + nuevo_cod
                data['codigo'] = nuevo_cod
            # Guardamos el Servicio creado
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
            elif action == 'confirm':
                usuarioAsignado = Usuarios.objects.all().last()
                # data = []
                # Asigno a una variable los parametros de estados y de tipos de usuarios
                estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                # Obtenemos los usuarios que puede realizar trabajos
                usuarios = Usuarios.objects.filter(realizaTrabajos=True)
                try:
                    # asignamos a una variable una cantidad alta de trabajos pendientes
                    cant = 1000000
                    # recorremos por cada usuario dentro del filtro anterior excluyendo trabajos finalizados en adelante
                    for user in usuarios:
                        trabajos = Trabajos.objects.filter(usuarioAsignado_id=user.id).exclude(
                            estadoTrabajo__orden__gte=estado.estadoFinalizado.orden).count()
                        if cant > trabajos:
                            usuarioAsignado = user
                            cant = trabajos
                    # data.append({'id': usuario.id, 'text': usuario.username})
                except Exception as e:
                    data['error'] = str(e)
                #     Comenzamos el proceso de Crear Trabajo
                with transaction.atomic():
                    formPresupuestoRequest = json.loads(request.POST['presupuesto'])
                    # Obtenemos el Presupuesto Base que se esta editando
                    presupuesto = self.get_object()
                    presupuesto.fecha = formPresupuestoRequest['fecha']
                    # obtenemos el Usuario actual
                    presupuesto.usuario = request.user
                    presupuesto.cliente_id = formPresupuestoRequest['cliente']
                    presupuesto.modelo_id = formPresupuestoRequest['modelo']
                    presupuesto.subtotal = float(formPresupuestoRequest['subtotal'])
                    presupuesto.iva = float(formPresupuestoRequest['iva'])
                    presupuesto.percepcion = float(formPresupuestoRequest['percepcion'])
                    presupuesto.total = float(formPresupuestoRequest['total'])
                    presupuesto.observaciones = formPresupuestoRequest['observaciones']
                    presupuesto.estado = True
                    presupuesto.save()
                    # Creamos una instancia de Trabajo
                    trabajo = Trabajos()
                    trabajo.fechaEntrada = date.today()
                    trabajo.usuario = request.user
                    trabajo.cliente_id = formPresupuestoRequest['cliente']
                    trabajo.modelo_id = formPresupuestoRequest['modelo']
                    trabajo.subtotal = float(formPresupuestoRequest['subtotal'])
                    trabajo.iva = float(formPresupuestoRequest['iva'])
                    trabajo.percepcion = float(formPresupuestoRequest['percepcion'])
                    trabajo.total = float(formPresupuestoRequest['total'])
                    # Asignamos el usuario que filtramos anteriormente
                    trabajo.usuarioAsignado = usuarioAsignado
                    trabajo.observaciones = formPresupuestoRequest['observaciones']
                    trabajo.prioridad_id = request.POST['prioridad']
                    # Obtenemos el nombre del estado en el ORDEN INICIAL
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        trabajo.estadoTrabajo_id = estado.estadoInicial_id
                    except Exception as e:
                        pass
                    trabajo.save()
                    # Se crea un evento de agenda por el trabajo confirmado
                    metodo_evento_asoc = ComprasCreateView()
                    descripcion = "Vence el plazo del trabajo Nro° " + str(trabajo.id) + \
                                  ", cliente " + trabajo.cliente.razonSocial + \
                                  " modelo " + trabajo.modelo.nombre + " según prioridad establecida."
                    fechaNotif = datetime.date.today() + datetime.timedelta(days=trabajo.prioridad.plazoPrioridad)
                    metodo_evento_asoc.crear_evento_asoc(descripcion, fechaNotif)

                    # Eliminamos todos los productos del Detalle
                    presupuesto.detalleproductospresupuesto_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoRequest['productos']:
                        det = DetalleProductosPresupuesto()
                        det.presupuesto_id = presupuesto.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Creamos las instancias de detalle con los productos correspondientes al trabajo a realizarse
                        detTrabajo = DetalleProductosTrabajo()
                        detTrabajo.trabajo_id = trabajo.id
                        detTrabajo.producto_id = i['id']
                        detTrabajo.cantidad = int(i['cantidad'])
                        detTrabajo.precio = float(i['precioVenta'])
                        detTrabajo.subtotal = float(i['subtotal'])
                        detTrabajo.save()
                    # Eliminamos todos los productos del Detalle
                    presupuesto.detalleserviciospresupuesto_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoRequest['servicios']:
                        det = DetalleServiciosPresupuesto()
                        det.presupuesto_id = presupuesto.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Creamos las instancias de detalle con los servicios correspondientes al trabajo a realizarse
                        detTrabajo = DetalleServiciosTrabajo()
                        detTrabajo.trabajo_id = trabajo.id
                        detTrabajo.servicio_id = i['id']
                        detTrabajo.cantidad = int(i['cantidad'])
                        detTrabajo.precio = float(i['precioVenta'])
                        detTrabajo.subtotal = float(i['subtotal'])
                        detTrabajo.save()
                    # Devolvemos en Data la ID del Presupuesto para poder generar la Boleta
                    data = {'id': presupuesto.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Confirmar Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'confirm'
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['categorias'] = Categorias.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        context['prioridades'] = Prioridades.objects.all()
        return context


class PresupuestosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Presupuestos
    form_class = PresupuestosForm
    template_name = 'presupuestos/create.html'
    success_url = reverse_lazy('presupuestos:presupuestos_list')
    permission_required = 'presupuestos.delete_presupuestos'
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
                    # Obtenemos el PRESUPUESTO que se esta editando
                    presupuesto = self.get_object()
                    # Eliminamos el Presupuesto
                    presupuesto.estado = False
                    presupuesto.save()
                    data['redirect'] = self.url_redirect
                    data['check'] = 'ok'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dar de Baja un Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class PresupuestosPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'presupuestos.view_presupuestos'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Armamos el Logo de la Empresa
            logo = "file://" + str(settings.MEDIA_ROOT) + str(empresa.imagen)
            # Utilizamos el template para generar el PDF
            template = get_template('presupuestos/pdf.html')
            # Obtenemos el subtotal de Productos y Servicios para visualizar en el template
            subtotalProductos = DetalleProductosPresupuesto.objects.filter(presupuesto_id=self.kwargs['pk'])
            subtotalServicios = DetalleServiciosPresupuesto.objects.filter(presupuesto_id=self.kwargs['pk'])
            # Obtenemos el valor total para pasar a letras
            total = Presupuestos.objects.get(pk=self.kwargs['pk']).total
            # Pasamos a letras el total
            totalEnLetras = NumeroALetras(total).a_letras.upper()
            productos = 0
            for i in subtotalProductos:
                productos += i.subtotal
            servicios = 0
            for i in subtotalServicios:
                servicios += i.subtotal
            context = {
                'presupuesto': Presupuestos.objects.get(pk=self.kwargs['pk']),
                'enLetras': totalEnLetras,
                'subtotalProductos': productos,
                'subtotalServicios': servicios,
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
        except Exception as e:
            pass

        return HttpResponseRedirect(reverse_lazy('presupuestos:presupuestos_list'))
