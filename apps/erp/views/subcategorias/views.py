from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.erp.forms import SubcategoriasForm
from apps.erp.models import Subcategorias
from apps.mixins import ValidatePermissionRequiredMixin


class SubcategoriasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Subcategorias
    template_name = 'subcategorias/list.html'
    permission_required = 'erp.view_subcategorias'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Subcategorias.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Subcategorías'
        context['create_url'] = reverse_lazy('erp:subcategorias_create')
        context['list_url'] = reverse_lazy('erp:subcategorias_list')
        context['entity'] = 'Subcategorías'
        return context


class SubcategoriasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Subcategorias
    form_class = SubcategoriasForm
    template_name = 'subcategorias/create.html'
    success_url = reverse_lazy('erp:subcategorias_list')
    permission_required = 'erp.add_subcategorias'
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
        context['title'] = 'Crear una Subcategoría'
        context['entity'] = 'Subcategorias'
        context['list_url'] = reverse_lazy('erp:subcategorias_list')
        context['action'] = 'add'
        return context


class SubcategoriasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Subcategorias
    form_class = SubcategoriasForm
    template_name = 'subcategorias/create.html'
    success_url = reverse_lazy('erp:subcategorias_list')
    permission_required = 'erp.change_subcategorias'
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
        context['title'] = 'Editar Subcategoría'
        context['entity'] = 'Subcategorías'
        context['list_url'] = reverse_lazy('erp:subcategorias_list')
        context['action'] = 'edit'
        return context


class SubcategoriasDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Subcategorias
    success_url = reverse_lazy('erp:subcategorias_list')
    permission_required = 'erp.delete_subcategorias'
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
        context['title'] = 'Eliminar Subcategoría'
        context['entity'] = 'Subcategorías'
        context['list_url'] = reverse_lazy('erp:subcategorias_list')
        return context
