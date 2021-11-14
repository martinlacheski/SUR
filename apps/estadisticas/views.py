from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, DecimalField, IntegerField, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.views.generic import TemplateView

from apps.erp.models import Ventas
from apps.mixins import ValidatePermissionRequiredMixin
from apps.trabajos.models import Trabajos


class TrabajosVentasView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'trabajos_ventas.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_trabajos_ventas':
                meses = []
                totales = []
                totalesAnterior = []
                trabajos = []
                trabajosAnterior = []
                try:
                    fecha_inicio_actual = datetime.now() - relativedelta(months=12)
                    fecha_inicio_anterior = datetime.now() - relativedelta(months=24)
                    for m in range(1, 13):
                        year = fecha_inicio_actual.year
                        mes = fecha_inicio_actual.month
                        yearAnterior = fecha_inicio_anterior.year
                        mesAnterior = fecha_inicio_anterior.month
                        total = Ventas.objects.filter(fecha__year=year, fecha__month=mes).aggregate(
                            r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                        totalAnterior = Ventas.objects.filter(fecha__year=yearAnterior, fecha__month=mesAnterior).aggregate(
                            r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                        cantidad = Trabajos.objects.filter(fechaSalida__year=year, fechaSalida__month=mes).aggregate(
                            r=Coalesce(Count('id'), 0, output_field=IntegerField())).get('r')
                        cantidadAnterior = Trabajos.objects.filter(fechaSalida__year=yearAnterior,
                                                                   fechaSalida__month=mesAnterior).aggregate(
                            r=Coalesce(Count('id'), 0, output_field=IntegerField())).get('r')
                        if mes == 1:
                            meses.append('Enero ' + str(year))
                        elif mes == 2:
                            meses.append('Febrero ' + str(year))
                        elif mes == 3:
                            meses.append('Marzo ' + str(year))
                        elif mes == 4:
                            meses.append('Abril ' + str(year))
                        elif mes == 5:
                            meses.append('Mayo ' + str(year))
                        elif mes == 6:
                            meses.append('Junio ' + str(year))
                        elif mes == 7:
                            meses.append('Julio ' + str(year))
                        elif mes == 8:
                            meses.append('Agosto ' + str(year))
                        elif mes == 9:
                            meses.append('Septiembre ' + str(year))
                        elif mes == 10:
                            meses.append('Octubre ' + str(year))
                        elif mes == 11:
                            meses.append('Noviembre ' + str(year))
                        elif mes == 12:
                            meses.append('Diciembre ' + str(year))
                        totales.append(float(total))
                        totalesAnterior.append(float(totalAnterior))
                        trabajos.append(cantidad)
                        trabajosAnterior.append(cantidadAnterior)
                        fecha_inicio_actual = fecha_inicio_actual + relativedelta(months=1)
                        fecha_inicio_anterior = fecha_inicio_anterior + relativedelta(months=1)
                except Exception as e:
                    print(e)
                data = {
                    'meses': meses,
                    'totales': totales,
                    'totalesAnterior': totalesAnterior,
                    'trabajos': trabajos,
                    'trabajosAnterior': trabajosAnterior
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadistica de Trabajos y Ventas'
        context['list_url'] = reverse_lazy('estadisticas:trabajos_ventas')
        context['entity'] = 'Estadística Trabajos y Ventas'
        return context


class ProductosServiciosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'productos_servicios.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_trabajos_ventas':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': ''
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadistica de Productos y Servicios'
        context['list_url'] = reverse_lazy('estadisticas:productos_servicios')
        context['entity'] = 'Estadística Productos y Servicios'
        return context


class ClientesTrabajosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'clientes_trabajos.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_trabajos_ventas':

                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': ''
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadistica de Productos y Servicios'
        context['list_url'] = reverse_lazy('estadisticas:productos_servicios')
        context['entity'] = 'Estadística Productos y Servicios'
        return context


class ModelosMasRealizadosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modelos_mas_realizados.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_trabajos_ventas':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': ''
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadistica de Modelos más realizados'
        context['list_url'] = reverse_lazy('estadisticas:modelos_mas_realizados')
        context['entity'] = 'Estadística Modelos más realizados'
        return context


class ProductosMasVendidosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'productos_mas_vendidos.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_trabajos_ventas':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': ''
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadistica de Productos más vendidos'
        context['list_url'] = reverse_lazy('estadisticas:productos_mas_vendidos')
        context['entity'] = 'Estadística Productos más vendidos'
        return context


class ServiciosMasRealizadosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'servicios_mas_realizados.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_trabajos_ventas':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': ''
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadistica de Servicios más realizados'
        context['list_url'] = reverse_lazy('estadisticas:servicios_mas_realizados')
        context['entity'] = 'Estadística Servicios más realizados'
        return context


class InsumosMasUtilizadosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'insumos_mas_utilizados.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_trabajos_ventas':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': ''
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadistica de insumos más utilizados'
        context['list_url'] = reverse_lazy('estadisticas:insumos_mas_utilizados')
        context['entity'] = 'Estadística Insumos más utilizados'
        return context
