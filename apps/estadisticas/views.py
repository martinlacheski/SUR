from datetime import datetime
from operator import itemgetter

from dateutil.relativedelta import relativedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, DecimalField, IntegerField, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.views.generic import TemplateView

from apps.erp.models import Ventas, DetalleProductosVenta, Productos, Servicios, DetalleServiciosVenta, Clientes
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import Modelos
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
                    for m in range(1, 14):
                        year = fecha_inicio_actual.year
                        mes = fecha_inicio_actual.month
                        yearAnterior = fecha_inicio_anterior.year
                        mesAnterior = fecha_inicio_anterior.month
                        total = Ventas.objects.filter(fecha__year=year, fecha__month=mes).aggregate(
                            r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                        totalAnterior = Ventas.objects.filter(fecha__year=yearAnterior,
                                                              fecha__month=mesAnterior).aggregate(
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
            elif action == 'get_trabajos_ventas_filtradas':
                dias = []
                totales = []
                totalesAnterior = []
                trabajos = []
                trabajosAnterior = []
                try:
                    desde = request.POST['desde']
                    desde = datetime.strptime(desde, "%Y-%m-%d").date()
                    desdeAnterior = desde - relativedelta(months=12)
                    hasta = request.POST['hasta']
                    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
                    diferencia = hasta - desde
                    for dia in range(0, diferencia.days + 1):
                        total = Ventas.objects.filter(fecha=desde).aggregate(
                            r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                        totalAnterior = Ventas.objects.filter(fecha=desdeAnterior).aggregate(
                            r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                        cantidad = Trabajos.objects.filter(fechaSalida=desde).aggregate(
                            r=Coalesce(Count('id'), 0, output_field=IntegerField())).get('r')
                        cantidadAnterior = Trabajos.objects.filter(fechaSalida=desdeAnterior).aggregate(
                            r=Coalesce(Count('id'), 0, output_field=IntegerField())).get('r')
                        totales.append(float(total))
                        totalesAnterior.append(float(totalAnterior))
                        trabajos.append(cantidad)
                        trabajosAnterior.append(cantidadAnterior)
                        dias.append(desde.strftime('%d-%m-%Y'))
                        desde = desde + relativedelta(days=1)
                        desdeAnterior = desdeAnterior + relativedelta(days=1)
                except Exception as e:
                    print(e)
                data = {
                    'dias': dias,
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
            if action == 'get_productos_servicios':
                meses = []
                productos = []
                servicios = []
                try:
                    fecha_inicio_actual = datetime.now() - relativedelta(months=12)
                    totalProductos = 0
                    totalServicios = 0
                    for m in range(1, 14):
                        year = fecha_inicio_actual.year
                        mes = fecha_inicio_actual.month
                        for prod in Productos.objects.filter():
                            totalProductos += DetalleProductosVenta.objects.filter(venta__fecha__year=year,
                                                                                   venta__fecha__month=mes,
                                                                                   producto_id=prod.id).aggregate(
                                r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        for serv in Servicios.objects.filter():
                            totalServicios += DetalleServiciosVenta.objects.filter(venta__fecha__year=year,
                                                                                   venta__fecha__month=mes,
                                                                                   servicio_id=serv.id).aggregate(
                                r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
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
                        productos.append(float(totalProductos))
                        servicios.append(float(totalServicios))
                        fecha_inicio_actual = fecha_inicio_actual + relativedelta(months=1)
                except Exception as e:
                    print(e)
                data = {
                    'meses': meses,
                    'productos': productos,
                    'servicios': servicios,
                }
            elif action == 'get_productos_servicios_filtradas':
                dias = []
                productos = []
                servicios = []
                try:
                    desde = request.POST['desde']
                    desde = datetime.strptime(desde, "%Y-%m-%d").date()
                    hasta = request.POST['hasta']
                    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
                    diferencia = hasta - desde
                    totalProductos = 0
                    totalServicios = 0
                    for dia in range(0, diferencia.days + 1):
                        for prod in Productos.objects.filter():
                            totalProductos += DetalleProductosVenta.objects.filter(venta__fecha=desde,
                                                                                   producto_id=prod.id).aggregate(
                                r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        for serv in Servicios.objects.filter():
                            totalServicios += DetalleServiciosVenta.objects.filter(venta__fecha=desde,
                                                                                   servicio_id=serv.id).aggregate(
                                r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        productos.append(float(totalProductos))
                        servicios.append(float(totalServicios))
                        dias.append(desde.strftime('%d-%m-%Y'))
                        totalProductos = 0
                        totalServicios = 0
                        desde = desde + relativedelta(days=1)
                except Exception as e:
                    print(e)
                data = {
                    'dias': dias,
                    'productos': productos,
                    'servicios': servicios,
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
            if action == 'get_ranking_inicial':
                datos = []
                try:
                    totalVentas = 0
                    totalTrabajos = 0
                    fecha_inicio_actual = datetime.now() - relativedelta(months=12)
                    for cli in Clientes.objects.all():
                        trabajos_filtrados = Trabajos.objects.filter(fechaSalida__gte=fecha_inicio_actual).filter(
                            cliente_id=cli.id)
                        totalTrabajos = len(trabajos_filtrados)
                        ventas_filtradas = Ventas.objects.filter(fecha__gte=fecha_inicio_actual).filter(
                            cliente_id=cli.id)
                        cantVentas = len(ventas_filtradas)
                        for vent in ventas_filtradas:
                            totalVentas += vent.total
                        if totalVentas > 0:
                            datos.append({
                                'cliente': cli.razonSocial,
                                'totales': float(totalVentas),
                                'ventas': cantVentas,
                                'trabajos': totalTrabajos
                            })
                        cantVentas = 0
                        totalVentas = 0
                        totalTrabajos = 0

                except Exception as e:
                    print(e)
                data = sorted(datos, key=itemgetter('totales'), reverse=True)
            elif action == 'get_ranking_filtrado':
                datos = []
                try:
                    desde = request.POST['desde']
                    desde = datetime.strptime(desde, "%Y-%m-%d").date()
                    hasta = request.POST['hasta']
                    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
                    totalVentas = 0
                    totalTrabajos = 0
                    for cli in Clientes.objects.all():
                        trabajos_filtrados = Trabajos.objects.filter(fechaSalida__gte=desde,
                                                                     fechaSalida__lte=hasta).filter(
                            cliente_id=cli.id)
                        totalTrabajos = len(trabajos_filtrados)
                        ventas_filtradas = Ventas.objects.filter(fecha__gte=desde, fecha__lte=hasta).filter(
                            cliente_id=cli.id)
                        cantVentas = len(ventas_filtradas)
                        for vent in ventas_filtradas:
                            totalVentas += vent.total
                        if totalVentas > 0:
                            datos.append({
                                'cliente': cli.razonSocial,
                                'totales': float(totalVentas),
                                'ventas': cantVentas,
                                'trabajos': totalTrabajos
                            })
                        cantVentas = 0
                        totalVentas = 0
                        totalTrabajos = 0
                except Exception as e:
                    print(e)
                print(datos)
                data = sorted(datos, key=itemgetter('totales'), reverse=True)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estadística Ranking de Clientes'
        context['list_url'] = reverse_lazy('estadisticas:clientes_trabajos')
        context['entity'] = 'Estadística Ranking Clientes'
        return context


class ModelosMasRealizadosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modelos_mas_realizados.html'

    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST['action']
            if action == 'get_ranking_modelos':
                try:
                    total = 0
                    fecha_inicio_actual = datetime.now() - relativedelta(months=12)
                    for mod in Modelos.objects.filter():
                        total = Trabajos.objects.filter(fechaSalida__gte=fecha_inicio_actual).filter(modelo_id=mod.id)
                        totalModelos = len(total)
                        if totalModelos > 0:
                            data.append({
                                'name': mod.marca.nombre + ' - ' + mod.nombre,
                                'y': float(totalModelos)
                            })
                except Exception as e:
                    print(e)
            elif action == 'get_ranking_filtrado':
                try:
                    total = 0
                    desde = request.POST['desde']
                    desde = datetime.strptime(desde, "%Y-%m-%d").date()
                    hasta = request.POST['hasta']
                    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
                    for mod in Modelos.objects.filter():
                        total = Trabajos.objects.filter(fechaSalida__gte=desde,
                                                        fechaSalida__lte=hasta).filter(modelo_id=mod.id)
                        totalModelos = len(total)
                        if totalModelos > 0:
                            data.append({
                                'name': mod.marca.nombre + ' - ' + mod.nombre,
                                'y': float(totalModelos)
                            })
                except Exception as e:
                    print(e)
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
        data = []
        try:
            action = request.POST['action']
            if action == 'get_ranking_productos':
                try:
                    total = 0
                    fecha_inicio_actual = datetime.now() - relativedelta(months=12)
                    for prod in Productos.objects.filter():
                        total = DetalleProductosVenta.objects.filter(venta__fecha__gte=fecha_inicio_actual,
                                                                     producto_id=prod.id).aggregate(
                            r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        if total > 0:
                            nombre = prod.abreviatura,
                            data.append({
                                'name': nombre,
                                'y': float(total)
                            })
                except Exception as e:
                    print(e)
            elif action == 'get_ranking_filtrado':
                try:
                    total = 0
                    desde = request.POST['desde']
                    desde = datetime.strptime(desde, "%Y-%m-%d").date()
                    hasta = request.POST['hasta']
                    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
                    for prod in Productos.objects.filter():
                        total = DetalleProductosVenta.objects.filter(venta__fecha__gte=desde, venta__fecha__lte=hasta,
                                                                     producto_id=prod.id).aggregate(
                            r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        if total > 0:
                            nombre = prod.abreviatura,
                            data.append({
                                'name': nombre,
                                'y': float(total)
                            })
                except Exception as e:
                    print(e)
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
        data = []
        try:
            action = request.POST['action']
            if action == 'get_ranking_servicios':
                try:
                    total = 0
                    fecha_inicio_actual = datetime.now() - relativedelta(months=12)
                    for serv in Servicios.objects.filter():
                        total = DetalleServiciosVenta.objects.filter(venta__fecha__gte=fecha_inicio_actual,
                                                                     servicio_id=serv.id).aggregate(
                            r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        if total > 0:
                            nombre = serv.descripcion,
                            data.append({
                                'name': nombre,
                                'y': float(total)
                            })
                except Exception as e:
                    print(e)
            elif action == 'get_ranking_filtrado':
                try:
                    total = 0
                    desde = request.POST['desde']
                    desde = datetime.strptime(desde, "%Y-%m-%d").date()
                    hasta = request.POST['hasta']
                    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
                    for serv in Servicios.objects.filter():
                        total = DetalleServiciosVenta.objects.filter(venta__fecha__gte=desde, venta__fecha__lte=hasta,
                                                                     servicio_id=serv.id).aggregate(
                            r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        if total > 0:
                            nombre = serv.descripcion,
                            data.append({
                                'name': nombre,
                                'y': float(total)
                            })
                except Exception as e:
                    print(e)
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
        data = []
        try:
            action = request.POST['action']
            if action == 'get_ranking_insumos':
                try:
                    total = 0
                    fecha_inicio_actual = datetime.now() - relativedelta(months=12)
                    for prod in Productos.objects.filter(esInsumo=True):
                        total = DetalleProductosVenta.objects.filter(venta__fecha__gte=fecha_inicio_actual,
                                                                     producto_id=prod.id).aggregate(
                            r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        if total > 0:
                            nombre = prod.abreviatura,
                            data.append({
                                'name': nombre,
                                'y': float(total)
                            })
                except Exception as e:
                    print(e)
            elif action == 'get_ranking_filtrado':
                try:
                    total = 0
                    desde = request.POST['desde']
                    desde = datetime.strptime(desde, "%Y-%m-%d").date()
                    hasta = request.POST['hasta']
                    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
                    for prod in Productos.objects.filter(esInsumo=True):
                        total = DetalleProductosVenta.objects.filter(venta__fecha__gte=desde, venta__fecha__lte=hasta,
                                                                     producto_id=prod.id).aggregate(
                            r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                        if total > 0:
                            nombre = prod.abreviatura,
                            data.append({
                                'name': nombre,
                                'y': float(total)
                            })
                except Exception as e:
                    print(e)
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
