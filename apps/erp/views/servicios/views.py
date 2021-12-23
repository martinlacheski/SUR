import datetime
import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from weasyprint import CSS, HTML

from apps.erp.forms import ServiciosForm
from apps.erp.models import Servicios
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import TiposIVA, Empresa
from config import settings


class ServiciosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Servicios
    template_name = 'servicios/list.html'
    permission_required = 'erp.view_servicios'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Servicios.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicios'
        context['create_url'] = reverse_lazy('erp:servicios_create')
        context['list_url'] = reverse_lazy('erp:servicios_list')
        context['entity'] = 'Servicios'
        return context


class ServiciosAuditListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Servicios
    template_name = 'servicios/audit.html'
    permission_required = 'erp.view_servicios'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Servicios.history.all():
                    try:
                        usuario = i.history_user.username
                    except:
                        usuario = '----'
                    dict = {'history_id': i.history_id, 'descripcion': i.descripcion, 'history_date': i.history_date,
                            'history_type': i.history_type, 'costo': i.costo, 'precioVenta': i.precioVenta,
                             'esfuerzo': i.esfuerzo, 'history_user': usuario}
                    data.append(dict)
            elif action == 'view_movimiento':
                data = []
                mov = Servicios.history.get(history_id=request.POST['pk'])
                movAnt = mov.prev_record
                try:
                    usuario = mov.history_user.username
                    movAnt = mov.prev_record
                except:
                    usuario = '----'
                if movAnt:
                    dict = {'descripcion': mov.descripcion, 'codigo': mov.codigo,
                        'costo': mov.costo, 'iva': mov.iva.nombre,
                        'precioVenta': mov.precioVenta, 'esfuerzo': mov.esfuerzo, 'imagen': mov.imagen,
                        'history_date': mov.history_date, 'history_type': mov.history_type, 'history_user': usuario,
                        'descripcionOld': movAnt.descripcion, 'codigoOld': movAnt.codigo,
                        'costoOld': movAnt.costo, 'ivaOld': movAnt.iva.nombre, 'precioVentaOld': movAnt.precioVenta,
                        'esfuerzoOld': movAnt.esfuerzo, 'imagenOld': movAnt.imagen}
                    data.append(dict)
                else:
                    dict = {'descripcion': mov.descripcion, 'codigo': mov.codigo,
                            'costo': mov.costo, 'iva': mov.iva.nombre,
                            'precioVenta': mov.precioVenta, 'esfuerzo': mov.esfuerzo, 'imagen': mov.imagen,
                            'history_date': mov.history_date, 'history_type': mov.history_type, 'history_user': usuario}
                    data.append(dict)
            elif action == 'create_reporte':
                # Traemos la empresa para obtener los valores
                empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
                # Armamos el Logo de la Empresa
                logo = "file://" + str(settings.MEDIA_ROOT) + str(empresa.imagen)
                # Utilizamos el template para generar el PDF
                template = get_template('servicios/reportAuditoria.html')
                # Obtenemos el detalle del Reporte
                reporte = json.loads(request.POST['reporte'])
                # Obtenemos el servicio si esta filtrado
                servicio = ""
                try:
                    servicio = reporte['servicio']
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
                servicios = []
                try:
                    servicios = reporte['servicios']
                    for serv in servicios:
                        serv['costo'] = float(serv['costo'])
                        serv['precioVenta'] = float(serv['precioVenta'])
                except Exception as e:
                    pass
                #   cargamos los datos del contexto
                try:
                    context = {
                        'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                                    'localidad': empresa.localidad.get_full_name(), 'imagen': logo},
                        'fecha': datetime.datetime.now(),
                        'servicio': servicio,
                        'accion': accion,
                        'inicio': inicio,
                        'fin': fin,
                        'servicios': servicios,
                        'usuarioAuditoria': usuario,
                        'usuario': request.user,
                    }
                    # Generamos el render del contexto
                    html = template.render(context)
                    # Asignamos la ruta donde se guarda el PDF
                    urlWrite = settings.MEDIA_ROOT + 'reporteAuditoriaServicios.pdf'
                    # Asignamos la ruta donde se visualiza el PDF
                    urlReporte = settings.MEDIA_URL + 'reporteAuditoriaServicios.pdf'
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
        context['title'] = 'Auditoría de Servicios'
        context['list_url'] = reverse_lazy('erp:servicios_audit')
        context['entity'] = 'Auditoría Servicios'
        return context


class ServiciosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Servicios
    form_class = ServiciosForm
    template_name = 'servicios/create.html'
    success_url = reverse_lazy('erp:servicios_list')
    permission_required = 'erp.add_servicios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'generar_codigo':
                try:
                    ultimo_serv = Servicios.objects.all().order_by('-id')[0]
                    nuevo_cod = str(ultimo_serv.id + 1)
                    if ultimo_serv.id <= 99999:
                        while len(nuevo_cod) <= 4:
                            nuevo_cod = '0' + nuevo_cod
                except:
                    nuevo_cod = '00001'
                data['codigo'] = nuevo_cod
            elif action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            elif action == 'add':
                form = self.get_form()
                data = form.save()
                data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('erp:servicios_list')
        context['action'] = 'add'
        return context


class ServiciosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Servicios
    form_class = ServiciosForm
    template_name = 'servicios/create.html'
    success_url = reverse_lazy('erp:servicios_list')
    permission_required = 'erp.change_servicios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            elif action == 'edit':
                form = self.get_form()
                data = form.save()
                data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('erp:servicios_list')
        context['action'] = 'edit'
        return context


class ServiciosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Servicios
    success_url = reverse_lazy('erp:servicios_list')
    permission_required = 'erp.delete_servicios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Captamos el ID y la Accion que viene del Template y realizamos la eliminacion logica
        id = request.POST['pk']
        action = request.POST['action']
        if action == 'delete':
            data = {}
            try:
                self.object.delete()
                data['redirect'] = self.url_redirect
                data['check'] = 'ok'
            except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('erp:servicios_list')
        return context
