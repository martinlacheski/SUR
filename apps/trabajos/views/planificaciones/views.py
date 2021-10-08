import json
import os
from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.erp.forms import ProductosForm, ServiciosForm, ClientesForm
from apps.erp.models import Productos, Servicios, Clientes, Ventas, Categorias, Subcategorias
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import MarcasForm, ModelosForm
from apps.parametros.models import Modelos, Empresa, Marcas, TiposIVA, EstadoParametros, CondicionesPago, MediosPago, \
    Estados
from apps.presupuestos.models import PlantillaPresupuestos, DetalleProductosPlantillaPresupuesto, \
    DetalleServiciosPlantillaPresupuesto, Presupuestos
from apps.trabajos.forms import TrabajosForm, PlanificacionesSemanalesForm
from apps.trabajos.models import Trabajos, DetalleProductosTrabajo, DetalleServiciosTrabajo, PlanificacionesSemanales
from config import settings

from weasyprint import HTML, CSS


class PlanificacionesSemanalesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = PlanificacionesSemanales
    template_name = 'planificaciones/list.html'
    permission_required = 'trabajos.view_planificacionessemanales'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in PlanificacionesSemanales.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Planificaciones Semanales'
        context['create_url'] = reverse_lazy('trabajos:planificaciones_create')
        context['list_url'] = reverse_lazy('trabajos:planificaciones_list')
        context['entity'] = 'Planificaciones Semanales'
        return context


class PlanificacionesSemanalesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = PlanificacionesSemanales
    form_class = PlanificacionesSemanalesForm
    template_name = 'planificaciones/create.html'
    success_url = reverse_lazy('trabajos:planificaciones_list')
    permission_required = 'trabajos.add_planificacionessemanales'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                try:
                    data = []
                    # Asigno a una variable los parametros de estados
                    estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                    # Obtengo los trabajos que estan pendientes de finalizarse
                    for i in Trabajos.objects.exclude(estadoTrabajo__orden__gte=estado.estadoFinalizado.orden):
                        data.append(i.toJSON())
                except Exception as e:
                    print(str(e))
            elif action == 'get_parametros_estados':
                data = []
                parametros = EstadoParametros.objects.get(id=EstadoParametros.objects.all().last().id)
                data.append(parametros.toJSON())
            elif action == 'add':
                form = self.get_form()
                data = form.save()
                data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Planificación Semanal'
        context['entity'] = 'Planificaciones Semanales'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PlanificacionesSemanalesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PlanificacionesSemanales
    form_class = PlanificacionesSemanalesForm
    template_name = 'planificaciones/create.html'
    success_url = reverse_lazy('trabajos:planificaciones_list')
    permission_required = 'trabajos.change_planificacionessemanales'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = TrabajosForm(instance=instance)
        # Obtenemos unicamente el MODELO y CLIENTE en el que se CREO el TRABAJO, para poder modificar el mismo
        form.fields['modelo'].queryset = Modelos.objects.filter(id=instance.modelo.id)
        form.fields['cliente'].queryset = Clientes.objects.filter(id=instance.cliente.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                pass
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar una Planificación Semanal'
        context['entity'] = 'Planificaciones Semanales'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PlanificacionesSemanalesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PlanificacionesSemanales
    form_class = PlanificacionesSemanalesForm
    template_name = 'planificaciones/create.html'
    success_url = reverse_lazy('trabajos:planificaciones_list')
    permission_required = 'trabajos.delete_planificacionessemanales'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                pass
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Planificación Semanal'
        context['entity'] = 'Planificaciones Semanales'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class PlanificacionesSemanalesPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'trabajos.view_planificacionessemanales'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Utilizamos el template para generar el PDF
            template = get_template('planificaciones/pdf.html')
            # Obtenemos el subtotal de Productos y Servicios para visualizar en el template
            planificacion = PlanificacionesSemanales.objects.get(id=self.kwargs['pk'])
            context = {
                'planificacion': PlanificacionesSemanales.objects.get(pk=self.kwargs['pk']),
                'inicio': planificacion.fechaInicio,
                'fin': planificacion.fechaFin,
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
            pass

        return HttpResponseRedirect(reverse_lazy('trabajos:planificaciones_list'))
