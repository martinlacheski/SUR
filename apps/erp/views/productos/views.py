import datetime
import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.erp.forms import ProductosForm, SubcategoriasForm, CategoriasForm
from apps.erp.models import Productos, Categorias, Subcategorias
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import TiposIVA, Empresa

from config import settings

from weasyprint import HTML, CSS


class ProductosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Productos
    template_name = 'productos/list.html'
    permission_required = 'erp.view_productos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Productos.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:productos_create')
        context['list_url'] = reverse_lazy('erp:productos_list')
        context['entity'] = 'Productos'
        return context


class ProductosAuditListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Productos
    template_name = 'productos/audit.html'
    permission_required = 'erp.view_productos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Productos.history.all():
                    try:
                        usuario = i.history_user.username
                    except:
                        usuario = '----'
                    dict = {'history_id': i.history_id, 'descripcion': i.descripcion, 'costo': i.costo,
                            'utilidad': i.utilidad, 'iva': i.iva.nombre, 'precioVenta': i.precioVenta,
                            'stockReal': i.stockReal, 'history_date': i.history_date,
                            'history_type': i.history_type, 'history_user': usuario}
                    data.append(dict)
            elif action == 'view_movimiento':
                data = []
                mov = Productos.history.get(history_id=request.POST['pk'])
                movAnt = mov.prev_record
                try:
                    usuario = mov.history_user.username
                    movAnt = mov.prev_record
                except:
                    usuario = '----'
                if movAnt:
                    dict = {'categoria': mov.subcategoria.categoria.nombre, 'subcategoria': mov.subcategoria.nombre,
                            'descripcion': mov.descripcion, 'abreviatura': mov.abreviatura,
                            'codigo': mov.codigo, 'codigoProveedor': mov.codigoProveedor,
                            'codigoBarras1': mov.codigoBarras1,
                            'stockReal': mov.stockReal, 'stockMinimo': mov.stockMinimo, 'reposicion': mov.reposicion,
                            'costo': mov.costo, 'utilidad': mov.utilidad, 'iva': mov.iva.nombre,
                            'precioVenta': mov.precioVenta, 'imagen': mov.imagen, 'ubicacion': mov.ubicacion,
                            'observaciones': mov.observaciones, 'esInsumo': mov.esInsumo,
                            'descuentaStock': mov.descuentaStock,
                            'history_date': mov.history_date, 'history_type': mov.history_type, 'history_user': usuario,
                            'categoriaOld': movAnt.subcategoria.categoria.nombre,
                            'subcategoriaOld': movAnt.subcategoria.nombre,
                            'descripcionOld': movAnt.descripcion, 'abreviaturaOld': movAnt.abreviatura,
                            'codigoOld': movAnt.codigo, 'codigoProveedorOld': movAnt.codigoProveedor,
                            'codigoBarras1Old': movAnt.codigoBarras1,
                            'stockRealOld': movAnt.stockReal, 'stockMinimoOld': movAnt.stockMinimo,
                            'reposicionOld': movAnt.reposicion,
                            'costoOld': movAnt.costo, 'utilidadOld': movAnt.utilidad,
                            'ivaOld': movAnt.iva.nombre,
                            'precioVentaOld': movAnt.precioVenta, 'imagenOld': movAnt.imagen,
                            'ubicacionOld': movAnt.ubicacion,
                            'observacionesOld': movAnt.observaciones, 'esInsumoOld': movAnt.esInsumo,
                            'descuentaStockOld': movAnt.descuentaStock}
                    data.append(dict)
                else:
                    dict = {'categoria': mov.subcategoria.categoria.nombre, 'subcategoria': mov.subcategoria.nombre,
                            'descripcion': mov.descripcion, 'abreviatura': mov.abreviatura,
                            'codigo': mov.codigo, 'codigoProveedor': mov.codigoProveedor,
                            'codigoBarras1': mov.codigoBarras1,
                            'stockReal': mov.stockReal, 'stockMinimo': mov.stockMinimo, 'reposicion': mov.reposicion,
                            'costo': mov.costo, 'utilidad': mov.utilidad, 'iva': mov.iva.nombre,
                            'precioVenta': mov.precioVenta, 'imagen': mov.imagen, 'ubicacion': mov.ubicacion,
                            'observaciones': mov.observaciones, 'esInsumo': mov.esInsumo,
                            'descuentaStock': mov.descuentaStock,
                            'history_date': mov.history_date, 'history_type': mov.history_type, 'history_user': usuario}
                    data.append(dict)
            elif action == 'create_reporte':
                # Traemos la empresa para obtener los valores
                empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
                # Utilizamos el template para generar el PDF
                template = get_template('productos/reportAuditoria.html')
                # Obtenemos el detalle del Reporte
                reporte = json.loads(request.POST['reporte'])
                # Obtenemos el producto si esta filtrado
                producto = ""
                try:
                    producto = reporte['producto']
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
                productos = []
                try:
                    productos = reporte['productos']
                    for prod in productos:
                        prod['costo'] = float(prod['costo'])
                        prod['utilidad'] = float(prod['utilidad'])
                        prod['precioVenta'] = float(prod['precioVenta'])
                except Exception as e:
                    pass
                #   cargamos los datos del contexto
                try:
                    context = {
                        'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                                    'localidad': empresa.localidad.get_full_name(), 'imagen': empresa.imagen},
                        'fecha': datetime.datetime.now(),
                        'producto': producto,
                        'accion': accion,
                        'inicio': inicio,
                        'fin': fin,
                        'productos': productos,
                        'usuarioAuditoria': usuario,
                        'usuario': request.user,
                    }
                    # Generamos el render del contexto
                    html = template.render(context)
                    # Asignamos la ruta donde se guarda el PDF
                    urlWrite = settings.MEDIA_ROOT + 'reportes/reporteAuditoriaProductos.pdf'
                    # Asignamos la ruta donde se visualiza el PDF
                    urlReporte = settings.MEDIA_URL + 'reportes/reporteAuditoriaProductos.pdf'
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
        context['title'] = 'Auditoría de Productos'
        context['list_url'] = reverse_lazy('erp:productos_audit')
        context['entity'] = 'Auditoría Productos'
        return context


class ProductosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/create.html'
    success_url = reverse_lazy('erp:productos_list')
    permission_required = 'erp.add_productos'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            elif action == 'search_categorias':
                data = [{'id': '', 'text': '---------'}]
                for i in Categorias.objects.all():
                    data.append({'id': i.id, 'text': i.nombre})
            elif action == 'search_subcategorias':
                data = [{'id': '', 'text': '---------'}]
                for i in Subcategorias.objects.filter(categoria_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            elif action == 'create_subcategoria':
                with transaction.atomic():
                    formSubcategoria = SubcategoriasForm(request.POST)
                    data = formSubcategoria.save()
            elif action == 'create_categoria':
                with transaction.atomic():
                    formCategoria = CategoriasForm(request.POST)
                    data = formCategoria.save()
            elif action == 'add':
                form = self.get_form()
                data = form.save()
                data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:productos_list')
        context['action'] = 'add'
        context['categorias'] = Categorias.objects.all()
        context['formSubcategoria'] = SubcategoriasForm()
        context['formCategoria'] = CategoriasForm()
        return context


class ProductosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/create.html'
    success_url = reverse_lazy('erp:productos_list')
    permission_required = 'erp.change_productos'
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
            if action == 'search_categorias':
                data = [{'id': '', 'text': '---------'}]
                for i in Categorias.objects.all():
                    data.append({'id': i.id, 'text': i.nombre})
            if action == 'search_subcategorias':
                data = [{'id': '', 'text': '---------'}]
                for i in Subcategorias.objects.filter(categoria_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            elif action == 'create_subcategoria':
                with transaction.atomic():
                    formSubcategoria = SubcategoriasForm(request.POST)
                    data = formSubcategoria.save()
            elif action == 'create_categoria':
                with transaction.atomic():
                    formCategoria = CategoriasForm(request.POST)
                    data = formCategoria.save()
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
        context['title'] = 'Editar Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:productos_list')
        context['action'] = 'edit'
        return context


class ProductosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Productos
    success_url = reverse_lazy('erp:productos_list')
    permission_required = 'erp.delete_productos'
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
        context['title'] = 'Eliminar Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:productos_list')
        return context
