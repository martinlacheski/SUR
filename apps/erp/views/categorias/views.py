from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from apps.erp.forms import CategoriasForm
from apps.erp.models import Categorias
from apps.mixins import ValidatePermissionRequiredMixin


class CategoriasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Categorias
    template_name = 'categorias/list.html'
    permission_required = 'erp.view_categorias'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Categorias.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorías'
        context['create_url'] = reverse_lazy('erp:categorias_create')
        context['list_url'] = reverse_lazy('erp:categorias_list')
        context['entity'] = 'Categorías'
        return context


class CategoriasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Categorias
    form_class = CategoriasForm
    template_name = 'categorias/create.html'
    success_url = reverse_lazy('erp:categorias_list')
    permission_required = 'erp.add_categorias'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
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
        context['title'] = 'Crear una Categoría'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:categorias_list')
        context['action'] = 'add'
        return context


class CategoriasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Categorias
    form_class = CategoriasForm
    template_name = 'categorias/create.html'
    success_url = reverse_lazy('erp:categorias_list')
    permission_required = 'erp.change_categorias'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
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
        context['title'] = 'Editar Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:categorias_list')
        context['action'] = 'edit'
        return context


class CategoriasDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Categorias
    success_url = reverse_lazy('erp:categorias_list')
    permission_required = 'erp.delete_categorias'
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
                data['check'] = str(e)
        return JsonResponse(data)

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:categorias_list')
        return context
