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
from apps.erp.models import Productos, Servicios
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import MarcasForm, ModelosForm
from apps.parametros.models import Modelos, Empresa, Marcas
from apps.presupuestos.forms import PresupuestosBaseForm
from apps.presupuestos.models import PresupuestosBase, DetalleProductosPresupuestoBase, DetalleServiciosPresupuestoBase
from config import settings

from weasyprint import HTML, CSS


class PresupuestosBaseListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = PresupuestosBase
    template_name = 'presupuestosBase/list.html'
    permission_required = 'presupuestos.view_presupuestosbase'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in PresupuestosBase.objects.all()[0:15]:
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosPresupuestoBase.objects.filter(presupuestoBase_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detalle_servicios':
                data = []
                for i in DetalleServiciosPresupuestoBase.objects.filter(presupuestoBase_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Presupuestos Base'
        context['create_url'] = reverse_lazy('presupuestos:presupuestosBase_create')
        context['list_url'] = reverse_lazy('presupuestos:presupuestosBase_list')
        context['entity'] = 'Presupuestos Base'
        return context


class PresupuestosBaseCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = PresupuestosBase
    form_class = PresupuestosBaseForm
    template_name = 'presupuestosBase/create.html'
    success_url = reverse_lazy('presupuestos:presupuestosBase_list')
    permission_required = 'presupuestos.add_presupuestosbase'
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
                    formPresupuestoBaseRequest = json.loads(request.POST['presupuestoBase'])
                    presupuestoBase = PresupuestosBase()
                    presupuestoBase.modelo_id = formPresupuestoBaseRequest['modelo']
                    presupuestoBase.descripcion = formPresupuestoBaseRequest['descripcion']
                    presupuestoBase.total = float(formPresupuestoBaseRequest['total'])
                    presupuestoBase.save()
                    for i in formPresupuestoBaseRequest['productos']:
                        det = DetalleProductosPresupuestoBase()
                        det.presupuestoBase_id = presupuestoBase.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    for i in formPresupuestoBaseRequest['servicios']:
                        det = DetalleServiciosPresupuestoBase()
                        det.presupuestoBase_id = presupuestoBase.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': presupuestoBase.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Presupuesto Base'
        context['entity'] = 'Presupuestos Base'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context


class PresupuestosBaseUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PresupuestosBase
    form_class = PresupuestosBaseForm
    template_name = 'presupuestosBase/create.html'
    success_url = reverse_lazy('presupuestos:presupuestosBase_list')
    permission_required = 'presupuestos.change_presupuestosbase'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PresupuestosBaseForm(instance=instance)
        # Obtenemos unicamente el MODELO en el que se CREO el PRESUPUESTO BASE, para poder modificar la misma
        form.fields['modelo'].queryset = Modelos.objects.filter(id=instance.modelo.id)
        return form

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
            # Buscamos los distintos productos ingresando por teclado
            if action == 'search_productos':
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
                    formPresupuestoBaseRequest = json.loads(request.POST['presupuestoBase'])
                    # Obtenemos el Presupuesto Base que se esta editando
                    presupuestoBase = self.get_object()
                    presupuestoBase.modelo_id = formPresupuestoBaseRequest['modelo']
                    presupuestoBase.descripcion = formPresupuestoBaseRequest['descripcion']
                    presupuestoBase.total = float(formPresupuestoBaseRequest['total'])
                    presupuestoBase.save()
                    # Eliminamos todos los productos del Detalle
                    presupuestoBase.detalleproductospresupuestobase_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoBaseRequest['productos']:
                        det = DetalleProductosPresupuestoBase()
                        det.presupuestoBase_id = presupuestoBase.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Eliminamos todos los productos del Detalle
                    presupuestoBase.detalleserviciospresupuestobase_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formPresupuestoBaseRequest['servicios']:
                        det = DetalleServiciosPresupuestoBase()
                        det.presupuestoBase_id = presupuestoBase.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Devolvemos en Data la ID del Presupuesto Base para poder generar la Boleta
                    data = {'id': presupuestoBase.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un Presupuesto Base'
        context['entity'] = 'Presupuestos Base'
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


class PresupuestosBaseDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PresupuestosBase
    form_class = PresupuestosBaseForm
    template_name = 'presupuestosBase/create.html'
    success_url = reverse_lazy('prespuestos:presupuestosBase_list')
    permission_required = 'presupuestos.delete_presupuestosBase'
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
                    # Obtenemos el PRESUPUESTO BASE que se esta editando
                    presupuestoBase = self.get_object()
                    # Eliminamos el Presupuesto Base
                    presupuestoBase.estado = False
                    presupuestoBase.save()
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
        context['title'] = 'Dar de Baja un Presupuesto Base'
        context['entity'] = 'Presupuestos Base'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class PresupuestosBasePdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'presupuestos.view_presupuestosbase'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(id=1)
            # Utilizamos el template para generar el PDF
            template = get_template('presupuestosBase/pdf.html')

            context = {
                'presupuestoBase': PresupuestosBase.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('presupuestos:presupuestoBase_list'))
