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

from apps.erp.forms import ProductosForm, ServiciosForm
from apps.erp.models import Productos, Servicios, Subcategorias, Categorias
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import MarcasForm, ModelosForm
from apps.parametros.models import Modelos, Empresa, Marcas, TiposIVA
from apps.presupuestos.forms import PresupuestosPlantillaForm
from apps.presupuestos.models import PlantillaPresupuestos, DetalleProductosPlantillaPresupuesto, \
    DetalleServiciosPlantillaPresupuesto
from config import settings

from weasyprint import HTML, CSS


class PresupuestosPlantillaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = PlantillaPresupuestos
    template_name = 'presupuestosPlantilla/list.html'
    permission_required = 'presupuestos.view_plantillapresupuestos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in PlantillaPresupuestos.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosPlantillaPresupuesto.objects.filter(
                        presupuestoPlantilla_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detalle_servicios':
                data = []
                for i in DetalleServiciosPlantillaPresupuesto.objects.filter(
                        presupuestoPlantilla_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Plantilla de Presupuestos'
        context['create_url'] = reverse_lazy('presupuestos:presupuestosPlantilla_create')
        context['list_url'] = reverse_lazy('presupuestos:presupuestosPlantilla_list')
        context['entity'] = 'Plantilla de Presupuestos'
        return context


class PresupuestosPlantillaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = PlantillaPresupuestos
    form_class = PresupuestosPlantillaForm
    template_name = 'presupuestosPlantilla/create.html'
    success_url = reverse_lazy('presupuestos:presupuestosPlantilla_list')
    permission_required = 'presupuestos.add_plantillapresupuestos'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # si no existe la marca la creamos
            if action == 'create_marca':
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
            elif action == 'add':
                with transaction.atomic():
                    formPresupuestoPlantillaRequest = json.loads(request.POST['presupuestoPlantilla'])
                    presupuestoPlantilla = PlantillaPresupuestos()
                    presupuestoPlantilla.modelo_id = formPresupuestoPlantillaRequest['modelo']
                    presupuestoPlantilla.descripcion = formPresupuestoPlantillaRequest['descripcion']
                    presupuestoPlantilla.save()
                    for i in formPresupuestoPlantillaRequest['productos']:
                        det = DetalleProductosPlantillaPresupuesto()
                        det.presupuestoPlantilla_id = presupuestoPlantilla.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.save()
                    for i in formPresupuestoPlantillaRequest['servicios']:
                        det = DetalleServiciosPlantillaPresupuesto()
                        det.presupuestoPlantilla_id = presupuestoPlantilla.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.save()
                    data = {'id': presupuestoPlantilla.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Plantilla de Presupuesto'
        context['entity'] = 'Plantilla de Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['categorias'] = Categorias.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context


class PresupuestosPlantillaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PlantillaPresupuestos
    form_class = PresupuestosPlantillaForm
    template_name = 'presupuestosPlantilla/create.html'
    success_url = reverse_lazy('presupuestos:presupuestosPlantilla_list')
    permission_required = 'presupuestos.change_plantillapresupuestos'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PresupuestosPlantillaForm(instance=instance)
        # Obtenemos unicamente el MODELO en el que se CREO la PLANTILLA DE PRESUPUESTO, para poder modificar la misma
        form.fields['modelo'].queryset = Modelos.objects.filter(id=instance.modelo.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosPlantillaPresupuesto.objects.filter(
                            presupuestoPlantilla_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosPlantillaPresupuesto.objects.filter(
                            presupuestoPlantilla_id=self.get_object().id):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
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
            elif action == 'edit':
                with transaction.atomic():
                    formPresupuestoPlantillaRequest = json.loads(request.POST['presupuestoPlantilla'])
                    # Obtenemos el Presupuesto Base que se esta editando
                    presupuestoPlantilla = self.get_object()
                    presupuestoPlantilla.modelo_id = formPresupuestoPlantillaRequest['modelo']
                    presupuestoPlantilla.descripcion = formPresupuestoPlantillaRequest['descripcion']
                    presupuestoPlantilla.save()
                    # Eliminamos todos los productos del Detalle
                    presupuestoPlantilla.detalleproductosplantillapresupuesto_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoPlantillaRequest['productos']:
                        det = DetalleProductosPlantillaPresupuesto()
                        det.presupuestoPlantilla_id = presupuestoPlantilla.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.save()
                    # Eliminamos todos los productos del Detalle
                    presupuestoPlantilla.detalleserviciosplantillapresupuesto_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoPlantillaRequest['servicios']:
                        det = DetalleServiciosPlantillaPresupuesto()
                        det.presupuestoPlantilla_id = presupuestoPlantilla.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.save()
                    # Devolvemos en Data la ID del Presupuesto Base para poder generar la Boleta
                    data = {'id': presupuestoPlantilla.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar una Plantilla de Presupuesto'
        context['entity'] = 'Plantilla de Presupuestos'
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


class PresupuestosPlantillaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PlantillaPresupuestos
    form_class = PresupuestosPlantillaForm
    template_name = 'presupuestosPlantilla/create.html'
    success_url = reverse_lazy('presupuestos:presupuestosPlantilla_list')
    permission_required = 'presupuestos.delete_plantillapresupuestos'
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
                    # Obtenemos la PLANTILLA de PRESUPUESTO que se esta editando
                    presupuestoPlantilla = self.get_object()
                    # Eliminamos el Presupuesto
                    presupuestoPlantilla.estado = False
                    presupuestoPlantilla.save()
                    data['redirect'] = self.url_redirect
                    data['check'] = 'ok'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dar de Baja una Plantilla de Presupuesto'
        context['entity'] = 'Plantilla de Presupuestos'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class PresupuestosPlantillaPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'presupuestos.view_plantillapresupuestos'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Armamos el Logo de la Empresa
            logo = "file://" + str(settings.MEDIA_ROOT) + str(empresa.imagen)
            # Utilizamos el template para generar el PDF
            template = get_template('presupuestosPlantilla/pdf.html')
            # Obtenemos el subtotal de Productos y Servicios para visualizar en el template
            context = {
                'presupuesto': PlantillaPresupuestos.objects.get(pk=self.kwargs['pk']),
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
            print(str(e))

        return HttpResponseRedirect(reverse_lazy('presupuestos:presupuestosPlantilla_list'))
