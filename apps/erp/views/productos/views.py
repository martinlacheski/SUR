from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.erp.forms import ProductosForm, SubcategoriasForm, CategoriasForm
from apps.erp.models import Productos, Categorias, Subcategorias
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import TiposIVA


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
                print(request.POST)
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
