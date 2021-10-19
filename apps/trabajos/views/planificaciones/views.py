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

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import Empresa, EstadoParametros
from apps.trabajos.forms import PlanificacionesSemanalesForm
from apps.trabajos.models import Trabajos, PlanificacionesSemanales, DetallePlanificacionesSemanales
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
                    item = i.toJSON()
                    # Incorporamos una variabla para poder obtener la cantidad de trabajos de la planificacion
                    cant = PlanificacionesSemanales.objects.get(id=i.id)
                    item['cantidad'] = cant.detalleplanificacionessemanales_set.count()
                    data.append(item)
            elif action == 'search_detalle_trabajos':
                data = []
                for i in DetallePlanificacionesSemanales.objects.filter(planificacion_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'get_parametros_estados':
                data = []
                parametros = EstadoParametros.objects.get(id=EstadoParametros.objects.all().last().id)
                data.append(parametros.toJSON())
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
                    data['error'] = str(e)
            elif action == 'get_parametros_estados':
                data = []
                parametros = EstadoParametros.objects.get(id=EstadoParametros.objects.all().last().id)
                data.append(parametros.toJSON())
            elif action == 'check_fechas_planificacion':
                inicio = request.POST['inicio']
                fin = request.POST['fin']
                # Buscamos si existen Planificaciones en ese rango de fechas
                try:
                    # planificaciones = PlanificacionesSemanales.objects.filter(fechaInicio__gte=inicio, fechaFin__lte=fin)
                    planificaciones = PlanificacionesSemanales.objects.filter(fechaInicio__range=[inicio, fin])
                    for i in planificaciones:
                        print(i.toJSON)
                    check = True
                    # planificaciones = PlanificacionesSemanales.objects.filter(fechaInicio__gte=inicio, fechaFin__lte=fin)
                    planificaciones = PlanificacionesSemanales.objects.filter(fechaFin__range=[inicio, fin])
                    for i in planificaciones:
                        print(i.toJSON)
                    check = True
                except Exception as e:
                    check = False
                data['check'] = check
            elif action == 'add':
                with transaction.atomic():
                    formPlanificacionRequest = json.loads(request.POST['planificacion'])
                    planificacion = PlanificacionesSemanales()
                    planificacion.fechaInicio = formPlanificacionRequest['fechaInicio']
                    planificacion.fechaFin = formPlanificacionRequest['fechaFin']
                    # obtenemos el Usuario actual
                    planificacion.usuario = request.user
                    planificacion.save()
                    # Inicializamos el orden de los trabajos
                    pos = 1
                    for i in formPlanificacionRequest['trabajos']:
                        det = DetallePlanificacionesSemanales()
                        det.planificacion_id = planificacion.id
                        det.trabajo_id = i['id']
                        # Buscamos el estado inicial del Proceso
                        try:
                            estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                            trabajoActual = Trabajos.objects.get(id=det.trabajo.id)
                            # Cambiamos el estado del trabajo a Planificado
                            trabajoActual.estadoTrabajo_id = estado.estadoPlanificado_id
                            trabajoActual.save()
                            det.orden = pos
                            det.save()
                            pos += 1
                        except Exception as e:
                            data['error'] = str(e)
                    # Devolvemos en Data la ID de la nueva Planificacion para poder generar la Boleta
                    data = {'id': planificacion.id}
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
        form = PlanificacionesSemanalesForm(instance=instance)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                try:
                    data = []
                    # Asigno a una variable los parametros de estados
                    estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                    # Obtengo los trabajos que no se encuentran en la planificacion
                    trabajos = []
                    for i in DetallePlanificacionesSemanales.objects.filter(planificacion_id=self.get_object().id):
                        trabajos.append(i.trabajo.id)
                    # Obtengo los trabajos que estan pendientes de finalizarse y que no estan en la planificacion
                    for i in Trabajos.objects.exclude(estadoTrabajo__orden__gte=estado.estadoFinalizado.orden).filter(
                            ~Q(id__in=trabajos)):
                        data.append(i.toJSON())
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_parametros_estados':
                data = []
                parametros = EstadoParametros.objects.get(id=EstadoParametros.objects.all().last().id)
                data.append(parametros.toJSON())
            # Metodo para obtener el detalle de los trabajos en la planificacion para mostrar en el template
            elif action == 'get_detalle_planificacion':
                data = []
                try:
                    for i in DetallePlanificacionesSemanales.objects.filter(planificacion_id=self.get_object().id):
                        item = i.trabajo.toJSON()
                        # item = i.toJSON()
                        # item['trabajo'] = i.trabajo.toJSON()
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'check_fechas_planificacion':
                inicio = request.POST['inicio']
                fin = request.POST['fin']
                # asignamos a una variable el ID de la planificacion actual
                planificacionID = self.kwargs['pk']
                # Buscamos si existen Planificaciones en ese rango de fechas
                # Filtramos por rango de fecha y excluimos el ID de la planificacion actual
                try:
                    planificaciones = PlanificacionesSemanales.objects.filter(fechaInicio__range=[inicio, fin]).exclude(id=planificacionID)
                    for i in planificaciones:
                        print(i.id)
                    check = True
                    print(planificaciones)
                    planificaciones = PlanificacionesSemanales.objects.filter(fechaFin__range=[inicio, fin]).exclude(id=planificacionID)
                    for i in planificaciones:
                        print(i.id)
                    check = True
                    print(planificaciones)
                except Exception as e:
                    check = False
                data['check'] = check
            elif action == 'edit':
                with transaction.atomic():
                    formPlanificacionRequest = json.loads(request.POST['planificacion'])
                    planificacion = self.get_object()
                    planificacion.fechaInicio = formPlanificacionRequest['fechaInicio']
                    planificacion.fechaFin = formPlanificacionRequest['fechaFin']
                    # obtenemos el Usuario actual
                    planificacion.usuario = request.user
                    planificacion.save()
                    # Eliminamos todos los Trabajos del Detalle
                    for i in formPlanificacionRequest['trabajos']:
                        # Buscamos el estado inicial del Proceso
                        try:
                            estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                            i.trabajo.estadoTrabajo_id = estado.estadoInicial_id
                        except Exception as e:
                            data['error'] = str(e)
                    planificacion.detalleplanificacionessemanales_set.all().delete()
                    # Inicializamos el orden de los trabajos
                    pos = 1
                    # Volvemos a cargar los Trabajos al Detalle
                    for i in formPlanificacionRequest['trabajos']:
                        det = DetallePlanificacionesSemanales()
                        det.planificacion_id = planificacion.id
                        det.trabajo_id = i['id']
                        # Buscamos el estado inicial del Proceso
                        try:
                            estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                            trabajoActual = Trabajos.objects.get(id=det.trabajo.id)
                            # Cambiamos el estado del trabajo a Planificado
                            trabajoActual.estadoTrabajo_id = estado.estadoPlanificado_id
                            trabajoActual.save()
                            det.orden = pos
                            det.save()
                            pos += 1
                        except Exception as e:
                            data['error'] = str(e)
                    # Devolvemos en Data la ID de la nueva Planificacion para poder generar la Boleta
                    data = {'id': planificacion.id}
                    data['redirect'] = self.url_redirect
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
        # Captamos la Accion que viene del Template y realizamos la eliminacion logica
        action = request.POST['action']
        if action == 'delete':
            data = {}
            try:
                id = self.object.id
                # Asignamos a una variable el detalle de trabajos de una planificacion
                trabajos = DetallePlanificacionesSemanales.objects.filter(planificacion_id=id)
                # Recorremos el detalle para cambiar el estado de los trabajos
                for i in trabajos:
                    # Buscamos el estado inicial del Proceso
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        # Actualizamos el estado a PENDIENTE en los Estados de Planificado
                        if i.trabajo.estadoTrabajo_id == estado.estadoPlanificado_id:
                            i.trabajo.estadoTrabajo_id = estado.estadoInicial_id
                            i.trabajo.save()
                    except Exception as e:
                        data['error'] = str(e)
                # Eliminamos todos los Trabajos del Detalle
                DetallePlanificacionesSemanales.objects.all().filter(planificacion_id=id).delete()
                # Eliminamos la planificacion
                self.object.delete()
                data['redirect'] = self.url_redirect
                data['check'] = 'ok'
            except Exception as e:
                print(str(e))
                data['error'] = str(e)
        return JsonResponse(data)

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
