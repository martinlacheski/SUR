from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.parametros.forms import MarcasForm
from apps.parametros.models import Marcas
from apps.mixins import ValidatePermissionRequiredMixin


class MarcasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Marcas
    template_name = 'marcas/list.html'
    permission_required = 'parametros.view_marcas'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Marcas.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Marcas'
        context['create_url'] = reverse_lazy('parametros:marcas_create')
        context['list_url'] = reverse_lazy('parametros:marcas_list')
        context['entity'] = 'Marcas'
        return context


class MarcasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Marcas
    form_class = MarcasForm
    template_name = 'marcas/create.html'
    success_url = reverse_lazy('parametros:marcas_list')
    permission_required = 'parametros.add_marcas'
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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Marca'
        context['entity'] = 'Marcas'
        context['list_url'] = reverse_lazy('parametros:marcas_list')
        context['action'] = 'add'
        return context


class MarcasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Marcas
    form_class = MarcasForm
    template_name = 'marcas/create.html'
    success_url = reverse_lazy('parametros:marcas_list')
    permission_required = 'parametros.change_marcas'
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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Marca'
        context['entity'] = 'Marcas'
        context['list_url'] = reverse_lazy('parametros:marcas_list')
        context['action'] = 'edit'
        return context


class MarcasDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Marcas
    success_url = reverse_lazy('parametros:marcas_list')
    permission_required = 'parametros.delete_marcas'
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
        return JsonResponse(data, safe=False)

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Marca'
        context['entity'] = 'Marcas'
        context['list_url'] = reverse_lazy('parametros:marcas_list')
        return context
