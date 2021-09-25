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

from apps.erp.forms import ComprasForm, ProveedoresForm, ProductosForm
from apps.erp.models import Compras, Productos, DetalleProductosCompra, Proveedores
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import Empresa, TiposIVA
from config import settings

from weasyprint import HTML, CSS


class ComprasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Compras
    template_name = 'compras/list.html'
    permission_required = 'erp.view_compras'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Compras.objects.all()[0:15]:
                    data.append(i.toJSON())
            elif action == 'search_detalle_productos':
                data = []
                for i in DetalleProductosCompra.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('erp:compras_create')
        context['list_url'] = reverse_lazy('erp:compras_list')
        context['entity'] = 'Compras'
        return context


class ComprasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Compras
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('erp:compras_list')
    permission_required = 'erp.add_compras'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # buscamos la percepcion del Proveedor
            if action == 'search_percepcion':
                proveedor = Proveedores.objects.get(id=request.POST['pk'])
                data['percepcion'] = proveedor.tipoPercepcion.percepcion
            # si no existe el Proveedor lo creamos
            elif action == 'create_proveedor':
                with transaction.atomic():
                    formProveedor = ProveedoresForm(request.POST)
                    data = formProveedor.save()
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
                        | Q(codigoBarras1__icontains=term)| Q(codigoBarras2__icontains=term))
                    item = producto.toJSON()
                    data['producto'] = item
                except Exception as e:
                    data['error'] = str(e)
            # Buscamos todos los productos
            elif action == 'search_all_productos':
                data = []
                for i in Productos.objects.all():
                    data.append(i.toJSON())
            # Buscamos el IVA para el MODAL de Productos
            elif action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            # si no existe el Producto lo creamos
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            elif action == 'add':
                with transaction.atomic():
                    formCompraRequest = json.loads(request.POST['compra'])
                    compra = Compras()
                    compra.fecha = formCompraRequest['fecha']
                    # obtenemos el Usuario actual
                    compra.usuario = request.user
                    compra.proveedor_id = formCompraRequest['proveedor']
                    compra.condicionPagoCompra_id = formCompraRequest['condicionPagoCompra']
                    compra.tipoComprobante_id = formCompraRequest['tipoComprobante']
                    compra.nroComprobante = formCompraRequest['nroComprobante']
                    compra.subtotal = float(formCompraRequest['subtotal'])
                    compra.iva = float(formCompraRequest['iva'])
                    compra.percepcion = float(formCompraRequest['percepcion'])
                    compra.total = float(formCompraRequest['total'])
                    compra.save()
                    for i in formCompraRequest['productos']:
                        det = DetalleProductosCompra()
                        print(i['costo'])
                        det.compra_id = compra.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.costo = float(i['costo'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Asignamos el Stock de los productos
                        det.producto.stockReal += det.cantidad
                        # Asignamos el costo de costo nuevo segun el importe de compra
                        det.producto.costo = det.costo
                        # Asignamos el precio de venta en base al costo
                        det.producto.precioVenta = float(det.costo) * ((float(det.producto.utilidad) / 100) + 1) * \
                                                   ((float(det.producto.iva.iva) / 100) + 1)
                        det.producto.save()
                    data = {'id': compra.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['formProveedor'] = ProveedoresForm()
        context['formProducto'] = ProductosForm()
        context['formPrecioProducto'] = ProductosForm()
        context['productos'] = Productos.objects.all()
        return context


class ComprasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Compras
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('erp:compras_list')
    permission_required = 'erp.change_compras'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = ComprasForm(instance=instance)
        # Obtenemos unicamente el PROVEEDOR en el que se CREO la COMPRA, para poder modificar la misma
        form.fields['proveedor'].queryset = Proveedores.objects.filter(id=instance.proveedor.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # buscamos la percepcion del cliente
            if action == 'search_percepcion':
                proveedor = Proveedores.objects.get(id=request.POST['pk'])
                data['percepcion'] = proveedor.tipoPercepcion.percepcion
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
            elif action == 'get_detalle_productos':
                data = []
                try:
                    for i in DetalleProductosCompra.objects.filter(compra_id=self.get_object().id):
                        item = i.producto.toJSON()
                        item['cantidad'] = i.cantidad
                        item['costo'] = i.costo
                        data.append(item)
                except Exception as e:
                    data['error'] = str(e)
            # Buscamos el IVA para el MODAL de Productos
            elif action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            # si no existe el Producto lo creamos
            elif action == 'create_producto':
                with transaction.atomic():
                    formProducto = ProductosForm(request.POST)
                    data = formProducto.save()
            elif action == 'edit':
                with transaction.atomic():
                    formCompraRequest = json.loads(request.POST['compra'])
                    # Obtenemos la compra que se esta editando
                    compra = self.get_object()
                    compra.fecha = formCompraRequest['fecha']
                    # obtenemos el Usuario actual
                    compra.usuario = request.user
                    compra.proveedor_id = formCompraRequest['proveedor']
                    compra.condicionPagoCompra_id = formCompraRequest['condicionPagoCompra']
                    compra.tipoComprobante_id = formCompraRequest['tipoComprobante']
                    compra.nroComprobante = formCompraRequest['nroComprobante']
                    compra.subtotal = float(formCompraRequest['subtotal'])
                    compra.iva = float(formCompraRequest['iva'])
                    compra.percepcion = float(formCompraRequest['percepcion'])
                    compra.total = float(formCompraRequest['total'])
                    compra.save()
                    # Reestablecemos el stock de los productos
                    for prod in DetalleProductosCompra.objects.filter(compra_id=self.get_object().id):
                        prod.producto.stockReal -= prod.cantidad
                        prod.producto.save()
                    # Eliminamos todos los productos del Detalle
                    compra.detalleproductoscompra_set.all().delete()
                    # Volvemos a cargar los productos al Detalle
                    for i in formCompraRequest['productos']:
                        det = DetalleProductosCompra()
                        det.compra_id = compra.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.costo = float(i['costo'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # Actualizamos el Stock de los Productos del Detalle
                        det.producto.stockReal += det.cantidad
                        # Asignamos el costo de costo nuevo segun el importe de compra
                        det.producto.costo = det.costo
                        # Asignamos el precio de venta en base al costo
                        det.producto.precioVenta = float(det.costo) * ((float(det.producto.utilidad) / 100) + 1) * \
                                                   ((float(det.producto.iva.iva) / 100) + 1)
                        det.producto.save()
                    # Devolvemos en Data la ID de la nueva Venta para poder generar la Boleta
                    data = {'id': compra.id}
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['formProveedor'] = ProveedoresForm()
        context['formProducto'] = ProductosForm()
        return context


class ComprasDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Compras
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('erp:compras_list')
    permission_required = 'erp.delete_compras'
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
                    # Obtenemos la compra que se esta editando
                    compra = self.get_object()
                    # Reestablecemos el stock de los productos
                    for prod in DetalleProductosCompra.objects.filter(compra_id=self.get_object().id):
                        prod.producto.stockReal -= prod.cantidad
                        prod.producto.save()
                    # Eliminamos la Compra
                    compra.estadoCompra = False
                    compra.save()
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
        context['title'] = 'Cancelar una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class ComprasPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'erp.view_compras'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(id=1)
            # Utilizamos el template para generar el PDF
            template = get_template('compras/pdf.html')

            context = {
                'compra': Compras.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('erp:compras_list'))