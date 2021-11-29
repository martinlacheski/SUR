import datetime
import json
import os
import random
from datetime import date

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
from apps.erp.models import Productos, Servicios, Clientes, Ventas, Categorias, Subcategorias, DetalleProductosVenta, \
    DetalleServiciosVenta
from apps.mixins import ValidatePermissionRequiredMixin
from apps.numlet import NumeroALetras
from apps.parametros.forms import MarcasForm, ModelosForm
from apps.parametros.models import Modelos, Empresa, Marcas, TiposIVA, EstadoParametros, CondicionesPago, MediosPago
from apps.presupuestos.models import PlantillaPresupuestos, DetalleProductosPlantillaPresupuesto, \
    DetalleServiciosPlantillaPresupuesto, Presupuestos
from apps.trabajos.forms import TrabajosForm
from apps.trabajos.models import Trabajos, DetalleProductosTrabajo, DetalleServiciosTrabajo
from apps.usuarios.models import Usuarios
from config import settings
from apps.bot_telegram.logicaBot import porcentajeTrabajo

from weasyprint import HTML, CSS

# Telegram notificacion
from apps.bot_telegram.management.commands.telegram_bot import notificarCliente

class TrabajosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Trabajos
    template_name = 'trabajos/list.html'
    permission_required = 'trabajos.view_trabajos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Trabajos.objects.all():
                    # Obtenemos el estado de avance por cada trabajo
                    totalEsfuerzo = 0
                    esfuerzoTrabRealizados = 0
                    detalle = DetalleServiciosTrabajo.objects.filter(trabajo_id=i.id)
                    # Calculamos el total del esfuerzo del trabajo y lo dividimos por el total de esfuerzo de servicios ya realizados
                    for d in detalle:
                        totalEsfuerzo += d.servicio.esfuerzo
                        if d.estado:
                            esfuerzoTrabRealizados += d.servicio.esfuerzo
                    if totalEsfuerzo != 0:
                        porcentaje = esfuerzoTrabRealizados / totalEsfuerzo
                    else:
                        porcentaje = 0
                    # Redondeamos para tener solo 2 decimales
                    porcentaje = round(round(porcentaje, 2) * 100, 2)
                    item = i.toJSON()
                    if i.usuarioAsignado:
                        item['asignado'] = i.usuarioAsignado.username
                    else:
                        item['asignado'] = 'EXPRESS'
                    item['porcentaje'] = str(porcentaje)
                    data.append(item)
            elif action == 'get_parametros_estados':
                data = []
                parametros = EstadoParametros.objects.get(id=EstadoParametros.objects.all().last().id)
                data.append(parametros.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosTrabajo.objects.filter(trabajo_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detalle_servicios':
                data = []
                for i in DetalleServiciosTrabajo.objects.filter(trabajo_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'create_reporte':
                # Traemos la empresa para obtener los valores
                empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
                # Utilizamos el template para generar el PDF
                template = get_template('trabajos/report.html')
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
                # Obtenemos el Usuario Asignado si esta filtrado
                usuarioAsignado = ""
                try:
                    usuarioAsignado = reporte['usuarioAsignado']
                except Exception as e:
                    pass
                # Obtenemos si se quito las Canceladas
                entregados = False
                try:
                    entregados = reporte['excluirEntregados']
                except Exception as e:
                    pass
                # Obtenemos si se quito las Canceladas
                cancelados = False
                try:
                    cancelados = reporte['excluirCancelados']
                except Exception as e:
                    pass
                # Obtenemos si se visualizan solo los pendientes
                pendientes = False
                try:
                    pendientes = reporte['verPendientes']
                except Exception as e:
                    pass
                # Obtenemos si se visualizan solo los planificados
                planificados = False
                try:
                    planificados = reporte['verPlanificados']
                except Exception as e:
                    pass
                # Obtenemos si se visualizan solo los En Proceso
                enProceso = False
                try:
                    enProceso = reporte['verEnProceso']
                except Exception as e:
                    pass
                # Obtenemos si se visualizan solo los Finalizados
                finalizados = False
                try:
                    finalizados = reporte['verFinalizados']
                except Exception as e:
                    pass
                # Obtenemos los trabajos
                trabajos = []
                try:
                    trabajos = reporte['trabajos']
                    for trabajo in trabajos:
                        trabajo['total'] = float(trabajo['total'])
                except Exception as e:
                    pass
                try:
                    estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                    estadoCancelado = estado.estadoCancelado.nombre
                except Exception as e:
                    pass
                total = 0
                neto = 0
                iva = 0
                percepcion = 0
                try:
                    for i in trabajos:
                        # Asignamos a una variable el estado de trabajo
                        estadoTrabajo = i['estadoTrabajo']
                        # Comparamos el nombre del estado de trabajo con el estado de trabajo en parametros
                        if estadoTrabajo['nombre'] != estado.estadoCancelado.nombre:
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
                        'modelo': modelo,
                        'inicio': inicio,
                        'fin': fin,
                        'usuarioAsignado': usuarioAsignado,
                        'entregados': entregados,
                        'cancelados': cancelados,
                        'pendientes': pendientes,
                        'planificados': planificados,
                        'enProceso': enProceso,
                        'finalizados': finalizados,
                        'trabajos': trabajos,
                        'estadoCancelado': estadoCancelado,
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
                    urlWrite = settings.MEDIA_ROOT + 'reporteTrabajos.pdf'
                    # Asignamos la ruta donde se visualiza el PDF
                    urlReporte = settings.MEDIA_URL + 'reporteTrabajos.pdf'
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
        context['title'] = 'Listado de Trabajos'
        context['create_url'] = reverse_lazy('trabajos:trabajos_create')
        context['list_url'] = reverse_lazy('trabajos:trabajos_list')
        context['entity'] = 'Trabajos'
        return context


class TrabajosAuditListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Trabajos
    template_name = 'trabajos/audit.html'
    permission_required = 'trabajos.view_trabajos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Trabajos.history.all():
                    try:
                        usuario = i.history_user.username
                    except:
                        usuario = '----'
                    dict = {'history_id': i.history_id, 'fechaEntrada': i.fechaEntrada, 'fechaSalida': i.fechaSalida,
                            'trabajo_id': i.id, 'subtotal': i.subtotal, 'iva': i.iva, 'percepcion': i.percepcion,
                            'total': i.total, 'fichaTrabajo': i.fichaTrabajo, 'observaciones': i.observaciones,
                            'history_date': i.history_date, 'history_type': i.history_type,
                            'cliente': i.cliente.razonSocial, 'estadoTrabajo': i.estadoTrabajo_id,
                            'modelo': i.modelo.nombre, 'prioridad': i.prioridad_id, 'history_user': usuario,
                            'usuarioAsignado': i.usuarioAsignado_id}
                    data.append(dict)
            elif action == 'view_movimiento':
                data = []
                mov = Trabajos.history.get(history_id=request.POST['pk'])
                tiempo_inicial = mov.history_date
                tiempo_margen = tiempo_inicial + datetime.timedelta(seconds=2)
                movAnt = mov.prev_record
                try:
                    usuario = mov.history_user.username
                    movAnt = mov.prev_record
                except:
                    usuario = '----'
                try:
                    usuarioAsignado = mov.usuarioAsignado.username
                except:
                    usuarioAsignado = '----'
                try:
                    usuarioAsignadoOld = movAnt.usuarioAsignado.username
                except:
                    usuarioAsignadoOld = '----'
                if movAnt:
                    dict = {'usuario': mov.usuario.username, 'history_id': mov.history_id,
                            'fechaEntrada': mov.fechaEntrada, 'fechaSalida': mov.fechaSalida, 'trabajo_id': mov.id,
                            'subtotal': mov.subtotal, 'iva': mov.iva, 'percepcion': mov.percepcion, 'total': mov.total,
                            'fichaTrabajo': mov.fichaTrabajo, 'observaciones': mov.observaciones,
                            'history_date': mov.history_date, 'history_type': mov.history_type,
                            'cliente': mov.cliente.razonSocial, 'estadoTrabajo': mov.estadoTrabajo.nombre,
                            'modelo': mov.modelo.nombre, 'prioridad': mov.prioridad.nombre, 'history_user': usuario,
                            'usuarioAsignado': usuarioAsignado,
                            'usuarioOld': movAnt.usuario.username, 'fechaEntradaOld': movAnt.fechaEntrada,
                            'fechaSalidaOld': movAnt.fechaSalida, 'subtotalOld': movAnt.subtotal, 'ivaOld': movAnt.iva,
                            'percepcionOld': movAnt.percepcion, 'totalOld': movAnt.total,
                            'fichaTrabajoOld': movAnt.fichaTrabajo, 'observacionesOld': movAnt.observaciones,
                            'history_dateOld': movAnt.history_date, 'history_typeOld': movAnt.history_type,
                            'clienteOld': movAnt.cliente.razonSocial, 'estadoTrabajoOld': movAnt.estadoTrabajo.nombre,
                            'modeloOld': movAnt.modelo.nombre, 'prioridadOld': movAnt.prioridad.nombre,
                            'history_userOld': usuario, 'usuarioAsignadoOld': usuarioAsignadoOld}
                    item = dict
                else:
                    dict = {'usuario': mov.usuario.username, 'history_id': mov.history_id,
                            'fechaEntrada': mov.fechaEntrada, 'fechaSalida': mov.fechaSalida, 'trabajo_id': mov.id,
                            'subtotal': mov.subtotal, 'iva': mov.iva, 'percepcion': mov.percepcion, 'total': mov.total,
                            'fichaTrabajo': mov.fichaTrabajo, 'observaciones': mov.observaciones,
                            'history_date': mov.history_date, 'history_type': mov.history_type,
                            'cliente': mov.cliente.razonSocial, 'estadoTrabajo': mov.estadoTrabajo.nombre,
                            'modelo': mov.modelo.nombre, 'prioridad': mov.prioridad.nombre, 'history_user': usuario,
                            'usuarioAsignado': mov.usuarioAsignado.username}
                    item = dict
                # Obtenemos el ID del trabajo para Filtrar
                trabajo = request.POST['trabajo_id']
                # Creamos un array de detalle de productos
                detalle_productos = []
                for i in DetalleProductosTrabajo.history.filter(trabajo_id=trabajo, history_date__range=[tiempo_inicial,
                                                                                                         tiempo_margen]).order_by(
                    'producto__descripcion'):
                    detalle = {
                        'producto': i.producto.descripcion, 'precio': i.precio, 'cantidad': i.cantidad,
                        'subtotal': i.subtotal, 'history_type': i.history_type, 'usuario': i.history_user.username,
                        'history_date': i.history_date, 'history_id': i.history_id}
                    detalle_productos.append(detalle)
                item['detalle_productos'] = detalle_productos
                # Creamos un array de detalle de servicios
                detalle_servicios = []
                for i in DetalleServiciosTrabajo.history.filter(trabajo_id=trabajo, history_date__range=[tiempo_inicial,
                                                                                                         tiempo_margen]).order_by(
                    'servicio__descripcion'):
                    detalle = {
                        'servicio': i.servicio.descripcion, 'precio': i.precio, 'cantidad': i.cantidad,
                        'subtotal': i.subtotal, 'history_type': i.history_type, 'usuario': i.history_user.username,
                        'history_date': i.history_date, 'history_id': i.history_id}
                    detalle_servicios.append(detalle)
                item['detalle_servicios'] = detalle_servicios
                data.append(item)
            # Creamos el REPORTE
            elif action == 'create_reporte':
                # Traemos la empresa para obtener los valores
                empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
                # Utilizamos el template para generar el PDF
                template = get_template('trabajos/reportAuditoria.html')
                # Obtenemos el detalle del Reporte
                reporte = json.loads(request.POST['reporte'])
                # Obtenemos el producto si esta filtrado
                trabajo = ""
                try:
                    trabajo = reporte['trabajo']
                except Exception as e:
                    pass
                # Obtenemos el usuario si esta filtrado
                usuario = ""
                try:
                    usuario = reporte['usuario']
                except Exception as e:
                    pass
                # Obtenemos el cliente si esta filtrado
                cliente = ""
                try:
                    cliente = reporte['cliente']
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
                trabajos = []
                try:
                    trabajos = reporte['trabajos']
                    for trab in trabajos:
                        trab['subtotal'] = float(trab['subtotal'])
                        trab['iva'] = float(trab['iva'])
                        trab['percepcion'] = float(trab['percepcion'])
                        trab['total'] = float(trab['total'])
                except Exception as e:
                    pass
                #   cargamos los datos del contexto
                try:
                    context = {
                        'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                                    'localidad': empresa.localidad.get_full_name(), 'imagen': empresa.imagen},
                        'fecha': datetime.datetime.now(),
                        'trabajo': trabajo,
                        'accion': accion,
                        'inicio': inicio,
                        'fin': fin,
                        'trabajos': trabajos,
                        'usuarioAuditoria': usuario,
                        'cliente': cliente,
                        'usuario': request.user,
                    }
                    # Generamos el render del contexto
                    html = template.render(context)
                    # Asignamos la ruta donde se guarda el PDF
                    urlWrite = settings.MEDIA_ROOT + 'reporteAuditoriaTrabajos.pdf'
                    # Asignamos la ruta donde se visualiza el PDF
                    urlReporte = settings.MEDIA_URL + 'reporteAuditoriaTrabajos.pdf'
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
        context['title'] = 'Auditoría de Trabajos'
        context['list_url'] = reverse_lazy('trabajos:trabajos_audit')
        context['entity'] = 'Auditoría Trabajos'
        return context


class TrabajosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Trabajos
    form_class = TrabajosForm
    template_name = 'trabajos/create.html'
    success_url = reverse_lazy('trabajos:trabajos_list')
    permission_required = 'trabajos.add_trabajos'
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
                for i in PlantillaPresupuestos.objects.filter(modelo_id=request.POST['pk']):
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
            # Asignamos automaticamente el trabajo al usuario mas desocupado
            elif action == 'get_mas_desocupado':
                data = []
                user_selecto = self.user_menos_ocupado()
                data.append(user_selecto)
                usuarios = Usuarios.objects.filter(realizaTrabajos=True).exclude(pk=user_selecto['id'])
                for u in usuarios:
                    data.append({'id': u.id, 'text': u.username})

            elif action == 'add':
                with transaction.atomic():
                    formTrabajoRequest = json.loads(request.POST['trabajo'])
                    trabajo = Trabajos()
                    trabajo.fechaEntrada = formTrabajoRequest['fechaEntrada']
                    # obtenemos el Usuario actual
                    trabajo.usuario = request.user
                    trabajo.cliente_id = formTrabajoRequest['cliente']
                    trabajo.modelo_id = formTrabajoRequest['modelo']
                    trabajo.usuarioAsignado_id = formTrabajoRequest['usuarioAsignado']
                    trabajo.subtotal = float(formTrabajoRequest['subtotal'])
                    trabajo.iva = float(formTrabajoRequest['iva'])
                    trabajo.percepcion = float(formTrabajoRequest['percepcion'])
                    trabajo.total = float(formTrabajoRequest['total'])
                    trabajo.prioridad_id = formTrabajoRequest['prioridad']
                    trabajo.observaciones = formTrabajoRequest['observaciones']
                    # Buscamos el estado inicial del Proceso
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        trabajo.estadoTrabajo_id = estado.estadoInicial_id
                    except Exception as e:
                        data['error'] = str(e)
                    trabajo.save()
                    for i in formTrabajoRequest['productos']:
                        det = DetalleProductosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    for i in formTrabajoRequest['servicios']:
                        det = DetalleServiciosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    # Devolvemos en Data la ID del nuevo Trabajo para poder generar la Boleta
                    data = {'id': trabajo.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Trabajo'
        context['entity'] = 'Trabajos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['formCliente'] = ClientesForm()
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['presupuestosPlantilla'] = PlantillaPresupuestos.objects.all()
        context['presupuestos'] = Presupuestos.objects.all()
        context['categorias'] = Categorias.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context

    def user_menos_ocupado(self):
        users_a_evaluar = Usuarios.objects.filter(realizaTrabajos=True)
        if len(users_a_evaluar) < 1:
            return {}
        else:
            # Se obtienen los estados de interés para los trabajos de los usuarios a evaluar
            estados = EstadoParametros.objects.last()
            estados_filter = [estados.estadoEspecial.id, estados.estadoInicial.id, estados.estadoPlanificado.id]
            # Se obtiene un diccionaro que sumariza cuantos trabajos y qué porcentaje de avance tiene cada usuario actualmente
            trab_por_user = []
            for u in users_a_evaluar:
                porcentaje_avance_trabajos = 0
                trabajos_user = Trabajos.objects.filter(usuarioAsignado=u,
                                                        estadoTrabajo__in=estados_filter)
                for t in trabajos_user:
                    porcentaje_avance_trabajos += float(porcentajeTrabajo(t))
                trab_por_user.append(
                    {'usuario': u,
                     'cant_trab': len(trabajos_user),
                     'procentaje_avance': porcentaje_avance_trabajos,
                    })
            # Ordenamiento de lista
            trab_por_user.sort(key=self.orden_cant_trab)
            # Se corrobora si existe un solo user con menor cantidad de trabajos.
            candidato = trab_por_user[0]
            users_candidatos = self.check_mas_de_uno(candidato, trab_por_user, 'cant_trab')
            if len(users_candidatos) == 1:
                return {'id': users_candidatos[0]['usuario'].id ,
                        'text':  users_candidatos[0]['usuario'].username}
            else:
                # Ordenamiento de lista
                trab_por_user.sort(key=self.orden_avance_trab)
                # Se corrobora si existe un solo user con mayor porcentaje de avance en trabajos.
                candidato = trab_por_user[0]
                users_candidatos = self.check_mas_de_uno(candidato, trab_por_user, 'procentaje_avance')
                if len(users_candidatos) == 1:
                    return {'id': users_candidatos[0]['usuario'].id,
                            'text': users_candidatos[0]['usuario'].username}
                else:
                    # Random
                    user_final = random.choice(users_candidatos)
                    return {'id': user_final['usuario'].id,
                            'text': user_final['usuario'].username}

    # Criterior de ordenación por cantidad de trabajos
    def orden_cant_trab(self, dict_user_trabajo):
        return dict_user_trabajo['cant_trab']

    # Criterior de ordenación por porcentaje de avance de trabajos
    def orden_avance_trab(self, dict_user_trabajo):
        return dict_user_trabajo['procentaje_avance']

    # Check si existe más de un user con el concepto que se le indique.
    # Returna lista de diccionarios.
    def check_mas_de_uno(self, candidato, trabajos, concepto):
        users_cand = []
        for u in trabajos:
            if u[concepto] == candidato[concepto]:
                users_cand.append(u)
        return users_cand



class TrabajosExpressCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Trabajos
    form_class = TrabajosForm
    template_name = 'trabajos/create.html'
    success_url = reverse_lazy('trabajos:trabajos_list')
    permission_required = 'trabajos.add_trabajos'
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
                for i in PlantillaPresupuestos.objects.filter(modelo_id=request.POST['pk']):
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
            elif action == 'express':
                with transaction.atomic():
                    formTrabajoRequest = json.loads(request.POST['trabajo'])
                    trabajo = Trabajos()
                    trabajo.fechaEntrada = formTrabajoRequest['fechaEntrada']
                    # obtenemos el Usuario actual
                    trabajo.usuario = request.user
                    trabajo.cliente_id = formTrabajoRequest['cliente']
                    trabajo.modelo_id = formTrabajoRequest['modelo']
                    # trabajo.usuarioAsignado_id = formTrabajoRequest['usuarioAsignado']
                    trabajo.subtotal = float(formTrabajoRequest['subtotal'])
                    trabajo.iva = float(formTrabajoRequest['iva'])
                    trabajo.percepcion = float(formTrabajoRequest['percepcion'])
                    trabajo.total = float(formTrabajoRequest['total'])
                    trabajo.prioridad_id = formTrabajoRequest['prioridad']
                    trabajo.observaciones = formTrabajoRequest['observaciones']
                    # Buscamos el estado Especial para iniciar el Proceso
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        trabajo.estadoTrabajo_id = estado.estadoEspecial_id
                    except Exception as e:
                        data['error'] = str(e)
                    trabajo.save()
                    for i in formTrabajoRequest['productos']:
                        det = DetalleProductosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            # det.fechaDetalle = datetime.datetime.now()
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    for i in formTrabajoRequest['servicios']:
                        det = DetalleServiciosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            # det.fechaDetalle = datetime.datetime.now()
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    # Devolvemos en Data la ID del nuevo Trabajo para poder generar la Boleta
                    data = {'id': trabajo.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Trabajo Express'
        context['entity'] = 'Trabajos'
        context['list_url'] = self.success_url
        context['action'] = 'express'
        context['formCliente'] = ClientesForm()
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['presupuestosPlantilla'] = PlantillaPresupuestos.objects.all()
        context['presupuestos'] = Presupuestos.objects.all()
        context['categorias'] = Categorias.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        return context


class TrabajosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Trabajos
    form_class = TrabajosForm
    template_name = 'trabajos/create.html'
    success_url = reverse_lazy('trabajos:trabajos_list')
    permission_required = 'trabajos.change_trabajos'
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
            # buscamos la percepcion del cliente
            if action == 'search_percepcion':
                cliente = Clientes.objects.get(id=request.POST['pk'])
                data['percepcion'] = cliente.tipoPercepcion.percepcion
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosTrabajo.objects.filter(trabajo_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        item['observaciones'] = i.observaciones
                        item['estado'] = i.estado
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosTrabajo.objects.filter(trabajo_id=self.get_object().id):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        item['observaciones'] = i.observaciones
                        item['estado'] = i.estado
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
                confirm = request.POST['confirm']
                with transaction.atomic():
                    formTrabajoRequest = json.loads(request.POST['trabajo'])
                    # Obtenemos el Trabajo que se esta editando
                    trabajo = self.get_object()
                    trabajo.fechaEntrada = formTrabajoRequest['fechaEntrada']
                    # obtenemos el Usuario actual
                    trabajo.usuario = request.user
                    trabajo.cliente_id = formTrabajoRequest['cliente']
                    trabajo.modelo_id = formTrabajoRequest['modelo']
                    trabajo.usuarioAsignado_id = formTrabajoRequest['usuarioAsignado']
                    trabajo.subtotal = float(formTrabajoRequest['subtotal'])
                    trabajo.iva = float(formTrabajoRequest['iva'])
                    trabajo.percepcion = float(formTrabajoRequest['percepcion'])
                    trabajo.total = float(formTrabajoRequest['total'])
                    trabajo.prioridad_id = formTrabajoRequest['prioridad']
                    trabajo.fichaTrabajo = formTrabajoRequest['fichaTrabajo']
                    trabajo.observaciones = formTrabajoRequest['observaciones']
                    # Buscamos el estado Especial para iniciar el Proceso
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        # Buscamos si hay un servicio ya realizado para cambiar el estado de Pendiente a En Proceso
                        for i in formTrabajoRequest['servicios']:
                            if i['estado'] == True:
                                trabajo.estadoTrabajo_id = estado.estadoEspecial_id
                        if confirm == 'si':
                            trabajo.estadoTrabajo_id = estado.estadoFinalizado_id
                        elif trabajo.estadoTrabajo_id == estado.estadoPlanificado_id:
                            trabajo.estadoTrabajo_id = estado.estadoEspecial_id
                    except Exception as e:
                        data['error'] = str(e)
                    trabajo.save()
                    if confirm == 'si':
                        notificarCliente(trabajo)
                    # Eliminamos todos los productos del Detalle
                    trabajo.detalleproductostrabajo_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formTrabajoRequest['productos']:
                        det = DetalleProductosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            # det.fechaDetalle = datetime.datetime.now()
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    # Eliminamos todos los productos del Detalle
                    trabajo.detalleserviciostrabajo_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formTrabajoRequest['servicios']:
                        det = DetalleServiciosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            # det.fechaDetalle = datetime.datetime.now()
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    # Devolvemos en Data la ID del nuevo Trabajo para poder generar la Boleta
                    data = {'id': trabajo.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un Trabajo'
        context['entity'] = 'Trabajos'
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


class TrabajosConfirmView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Trabajos
    form_class = TrabajosForm
    template_name = 'trabajos/create.html'
    success_url = reverse_lazy('trabajos:trabajos_list')
    permission_required = 'trabajos.change_trabajos'
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
            # buscamos la percepcion del cliente
            if action == 'search_percepcion':
                cliente = Clientes.objects.get(id=request.POST['pk'])
                data['percepcion'] = cliente.tipoPercepcion.percepcion
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosTrabajo.objects.filter(trabajo_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        item['observaciones'] = i.observaciones
                        item['estado'] = i.estado
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosTrabajo.objects.filter(trabajo_id=self.get_object().id):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        item['observaciones'] = i.observaciones
                        item['estado'] = i.estado
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
                with transaction.atomic():
                    formTrabajoRequest = json.loads(request.POST['trabajo'])
                    # Obtenemos el Trabajo que se esta editando
                    trabajo = self.get_object()
                    trabajo.fechaEntrada = formTrabajoRequest['fechaEntrada']
                    # trabajo.fechaSalida = date.today()
                    # obtenemos el Usuario actual
                    trabajo.usuario = request.user
                    trabajo.cliente_id = formTrabajoRequest['cliente']
                    trabajo.modelo_id = formTrabajoRequest['modelo']
                    trabajo.usuarioAsignado_id = formTrabajoRequest['usuarioAsignado']
                    trabajo.subtotal = float(formTrabajoRequest['subtotal'])
                    trabajo.iva = float(formTrabajoRequest['iva'])
                    trabajo.percepcion = float(formTrabajoRequest['percepcion'])
                    trabajo.total = float(formTrabajoRequest['total'])
                    trabajo.prioridad_id = formTrabajoRequest['prioridad']
                    trabajo.fichaTrabajo = formTrabajoRequest['fichaTrabajo']
                    trabajo.observaciones = formTrabajoRequest['observaciones']
                    # Obtenemos el nombre del estado en el ORDEN FINALIZADO
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        trabajo.estadoTrabajo_id = estado.estadoFinalizado_id

                    except Exception as e:
                        data['error'] = str(e)
                    trabajo.save()
                    notificarCliente(trabajo)
                    # Eliminamos todos los productos del Detalle
                    trabajo.detalleproductostrabajo_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formTrabajoRequest['productos']:
                        det = DetalleProductosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            # det.fechaDetalle = datetime.datetime.now()
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    # Eliminamos todos los productos del Detalle
                    trabajo.detalleserviciostrabajo_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formTrabajoRequest['servicios']:
                        det = DetalleServiciosTrabajo()
                        det.trabajo_id = trabajo.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.estado = i['estado']
                        try:
                            observacion = i['observaciones']
                        except Exception as e:
                            data['error'] = str(e)
                        if observacion != "":
                            det.observaciones = observacion
                            det.usuario = request.user
                            # det.fechaDetalle = datetime.datetime.now()
                            det.fechaDetalle = timezone.localtime(timezone.now())
                        det.save()
                    # Devolvemos en Data la ID del nuevo Trabajo para poder generar la Boleta
                    data = {'id': trabajo.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Confirmar Trabajo'
        context['entity'] = 'Trabajos'
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
        return context


class TrabajosDeliverView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Trabajos
    form_class = TrabajosForm
    template_name = 'trabajos/create.html'
    success_url = reverse_lazy('trabajos:trabajos_list')
    permission_required = 'trabajos.change_trabajos'
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
            # buscamos la percepcion del cliente
            if action == 'search_percepcion':
                cliente = Clientes.objects.get(id=request.POST['pk'])
                data['percepcion'] = cliente.tipoPercepcion.percepcion
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosTrabajo.objects.filter(trabajo_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        item['observaciones'] = i.observaciones
                        item['estado'] = i.estado
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            elif action == 'get_detalle_servicios':
                data = []
                try:
                    for i in DetalleServiciosTrabajo.objects.filter(trabajo_id=self.get_object().id):
                        item = i.servicio.toJSON()
                        item['cantidad'] = i.cantidad
                        item['precio'] = i.precio
                        item['observaciones'] = i.observaciones
                        item['estado'] = i.estado
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
            elif action == 'deliver':
                with transaction.atomic():
                    formTrabajoRequest = json.loads(request.POST['trabajo'])
                    # Obtenemos el Trabajo que se esta editando
                    trabajo = self.get_object()
                    trabajo.fechaEntrada = formTrabajoRequest['fechaEntrada']
                    trabajo.fechaSalida = date.today()
                    # obtenemos el Usuario actual
                    trabajo.usuario = request.user
                    trabajo.cliente_id = formTrabajoRequest['cliente']
                    trabajo.modelo_id = formTrabajoRequest['modelo']
                    trabajo.usuarioAsignado_id = formTrabajoRequest['usuarioAsignado']
                    trabajo.subtotal = float(formTrabajoRequest['subtotal'])
                    trabajo.iva = float(formTrabajoRequest['iva'])
                    trabajo.percepcion = float(formTrabajoRequest['percepcion'])
                    trabajo.total = float(formTrabajoRequest['total'])
                    trabajo.prioridad_id = formTrabajoRequest['prioridad']
                    trabajo.fichaTrabajo = formTrabajoRequest['fichaTrabajo']
                    trabajo.observaciones = formTrabajoRequest['observaciones']
                    # Obtenemos el nombre del estado en el ORDEN ENTREGADO
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        trabajo.estadoTrabajo_id = estado.estadoEntregado_id
                    except Exception as e:
                        data['error'] = str(e)
                    trabajo.save()
                    # Creamos una instancia de venta
                    venta = Ventas()
                    venta.fecha = date.today()
                    # obtenemos el Usuario actual
                    venta.usuario = request.user
                    venta.cliente_id = formTrabajoRequest['cliente']
                    # Traemos del POST la condicion de venta y el medio de pago
                    venta.condicionVenta_id = request.POST['condicionVenta']
                    venta.medioPago_id = request.POST['medioPago']
                    venta.subtotal = float(formTrabajoRequest['subtotal'])
                    venta.iva = float(formTrabajoRequest['iva'])
                    venta.percepcion = float(formTrabajoRequest['percepcion'])
                    venta.total = float(formTrabajoRequest['total'])
                    venta.trabajo = trabajo.id
                    venta.save()
                    # Creamos el detalle de Productos
                    for i in formTrabajoRequest['productos']:
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
                    # Creamos el detalle de Servicios
                    for i in formTrabajoRequest['servicios']:
                        det = DetalleServiciosVenta()
                        det.venta_id = venta.id
                        det.servicio_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precioVenta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # Devolvemos en Data la ID del nuevo Trabajo para poder generar la Boleta
                    data = {'id': trabajo.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Entregar Trabajo'
        context['entity'] = 'Trabajos'
        context['list_url'] = self.success_url
        context['action'] = 'deliver'
        context['formProducto'] = ProductosForm()
        context['formServicio'] = ServiciosForm()
        context['formMarca'] = MarcasForm()
        context['formModelo'] = ModelosForm()
        context['marcas'] = Marcas.objects.all()
        context['categorias'] = Categorias.objects.all()
        context['productos'] = Productos.objects.all()
        context['servicios'] = Servicios.objects.all()
        context['condicionesPago'] = CondicionesPago.objects.all()
        context['mediosPago'] = MediosPago.objects.all()
        return context


class TrabajosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Trabajos
    form_class = TrabajosForm
    template_name = 'trabajos/create.html'
    success_url = reverse_lazy('trabajos:trabajos_list')
    permission_required = 'trabajos.delete_trabajos'
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
                    # Obtenemos el TRABAJO que se esta editando
                    trabajo = self.get_object()
                    # Cancelamos el TRABAJO
                    trabajo.fechaSalida = date.today()
                    # Obtenemos el nombre del estado en el ORDEN CANCELADO
                    try:
                        estado = EstadoParametros.objects.get(pk=EstadoParametros.objects.all().last().id)
                        trabajo.estadoTrabajo_id = estado.estadoCancelado_id
                    except Exception as e:
                        data['error'] = str(e)
                    trabajo.save()
                    data['redirect'] = self.url_redirect
                    data['check'] = 'ok'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dar de Baja un Trabajo'
        context['entity'] = 'Trabajos'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class TrabajosPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'trabajos.view_trabajos'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Utilizamos el template para generar el PDF
            template = get_template('trabajos/pdf.html')
            # Obtenemos el subtotal de Productos y Servicios para visualizar en el template
            subtotalProductos = DetalleProductosTrabajo.objects.filter(trabajo_id=self.kwargs['pk'])
            subtotalServicios = DetalleServiciosTrabajo.objects.filter(trabajo_id=self.kwargs['pk'])
            # Obtenemos el valor total para pasar a letras
            total = Trabajos.objects.get(pk=self.kwargs['pk']).total
            # Pasamos a letras el total
            totalEnLetras = NumeroALetras(total).a_letras.upper()
            productos = 0
            for i in subtotalProductos:
                productos += i.subtotal
            servicios = 0
            for i in subtotalServicios:
                servicios += i.subtotal
            context = {
                'trabajo': Trabajos.objects.get(pk=self.kwargs['pk']),
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
        except Exception as e:
            pass
        return HttpResponseRedirect(reverse_lazy('trabajos:trabajos_list'))
