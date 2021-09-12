from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.parametros.forms import ModelosForm
from apps.parametros.models import Modelos
from apps.mixins import ValidatePermissionRequiredMixin


class ModelosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Modelos
    template_name = 'modelos/list.html'
    permission_required = 'parametros.view_modelos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Modelos.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Modelos'
        context['create_url'] = reverse_lazy('parametros:modelos_create')
        context['list_url'] = reverse_lazy('parametros:modelos_list')
        context['entity'] = 'Modelos'
        return context


class ModelosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Modelos
    form_class = ModelosForm
    template_name = 'modelos/create.html'
    success_url = reverse_lazy('parametros:modelos_list')
    permission_required = 'parametros.add_modelos'
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
        context['title'] = 'Crear un Modelo'
        context['entity'] = 'Modelos'
        context['list_url'] = reverse_lazy('parametros:modelos_list')
        context['action'] = 'add'
        return context


class ModelosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Modelos
    form_class = ModelosForm
    template_name = 'modelos/create.html'
    success_url = reverse_lazy('parametros:modelos_list')
    permission_required = 'parametros.change_modelos'
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
        context['title'] = 'Editar Modelo'
        context['entity'] = 'Modelos'
        context['list_url'] = reverse_lazy('parametros:modelos_list')
        context['action'] = 'edit'
        return context


class ModelosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Modelos
    success_url = reverse_lazy('parametros:modelos_list')
    permission_required = 'parametros.delete_modelos'
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
        context['title'] = 'Eliminar Modelo'
        context['entity'] = 'Modelos'
        context['list_url'] = reverse_lazy('parametros:modelos_list')
        return context
