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

from apps.erp.forms import ProductosForm, ServiciosForm, ClientesForm
from apps.erp.models import Productos, Servicios, Clientes
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import MarcasForm, ModelosForm
from apps.parametros.models import Modelos, Empresa, Marcas
from apps.presupuestos.forms import PresupuestosForm
from apps.presupuestos.models import Presupuestos, DetalleProductosPresupuesto, DetalleServiciosPresupuesto, \
    PresupuestosBase, DetalleProductosPresupuestoBase, DetalleServiciosPresupuestoBase
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
                for i in Presupuestos.objects.all()[0:15]:
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosPresupuesto.objects.filter(presupuesto_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detalle_servicios':
                data = []
                for i in DetalleServiciosPresupuesto.objects.filter(presupuesto_id=request.POST['id']):
                    data.append(i.toJSON())
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
            elif action == 'search_modelos':
                data = [{'id': '', 'text': '---------'}]
                for i in Modelos.objects.filter(marca_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            # Buscamos las plantillas de Presupuestos creadas
            elif action == 'search_plantillas':
                data = [{'id': '', 'text': '---------'}]
                for i in PresupuestosBase.objects.filter(modelo_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.get_full_name()})
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosPresupuestoBase.objects.filter(presupuestoBase_id=request.POST['pk']):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.producto.precioVenta
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosPresupuestoBase.objects.filter(presupuestoBase_id=request.POST['pk']):
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
                        | Q(codigoBarras1__icontains=term) | Q(codigoBarras2__icontains=term))
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
            # si no existe el Producto lo creamos
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # si no existe el Servicio lo creamos
            elif action == 'create_servicio':
                with transaction.atomic():
                    formServicio = ServiciosForm(request.POST)
                    data = formServicio.save()
            elif action == 'add':
                with transaction.atomic():
                    formPresupuestoRequest = json.loads(request.POST['presupuesto'])
                    presupuesto = Presupuestos()
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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['formCliente'] = ClientesForm()
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['presupuestosBase'] = PresupuestosBase.objects.all()
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
            if action == 'get_detalle_productos':
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
                        | Q(codigoBarras1__icontains=term) | Q(codigoBarras2__icontains=term))
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
            # si no existe el Producto lo creamos
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            # si no existe el Servicio lo creamos
            elif action == 'create_servicio':
                with transaction.atomic():
                    formServicio = ServiciosForm(request.POST)
                    data = formServicio.save()
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
        context['title'] = 'Editar un Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
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
            empresa = Empresa.objects.get(id=1)
            # Utilizamos el template para generar el PDF
            template = get_template('presupuestos/pdf.html')
            # Obtenemos el subtotal de Productos y Servicios para visualizar en el template
            subtotalProductos = DetalleProductosPresupuesto.objects.filter(presupuesto_id=self.kwargs['pk'])
            subtotalServicios = DetalleServiciosPresupuesto.objects.filter(presupuesto_id=self.kwargs['pk'])
            productos = 0
            for i in subtotalProductos:
                productos += i.subtotal
            servicios = 0
            for i in subtotalServicios:
                servicios += i.subtotal
            context = {
                'presupuesto': Presupuestos.objects.get(pk=self.kwargs['pk']),
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
        except Exception as e:
            print(str(e))

        return HttpResponseRedirect(reverse_lazy('presupuestos:presupuestos_list'))
