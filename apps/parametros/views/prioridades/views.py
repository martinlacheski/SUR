from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import PrioridadesForm
from apps.parametros.models import Prioridades


class PrioridadesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Prioridades
    template_name = 'prioridades/list.html'
    permission_required = 'parametros.view_prioridades'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Prioridades.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Prioridades de Trabajo'
        context['create_url'] = reverse_lazy('parametros:prioridades_create')
        context['list_url'] = reverse_lazy('parametros:prioridades_list')
        context['entity'] = 'Prioridades de Trabajo'
        return context


class PrioridadesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Prioridades
    form_class = PrioridadesForm
    template_name = 'prioridades/create.html'
    success_url = reverse_lazy('parametros:prioridades_list')
    permission_required = 'parametros.add_prioridades'
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
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Prioridad de Trabajo'
        context['entity'] = 'Prioridades de Trabajo'
        context['list_url'] = reverse_lazy('parametros:prioridades_list')
        context['action'] = 'add'
        return context


class PrioridadesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Prioridades
    form_class = PrioridadesForm
    template_name = 'prioridades/create.html'
    success_url = reverse_lazy('parametros:prioridades_list')
    permission_required = 'parametros.change_prioridades'
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
        context['title'] = 'Editar Prioridad de Trabajo'
        context['entity'] = 'Prioridades de Trabajo'
        context['list_url'] = reverse_lazy('parametros:prioridades_list')
        context['action'] = 'edit'
        return context


class PrioridadesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Prioridades
    success_url = reverse_lazy('parametros:prioridades_list')
    permission_required = 'parametros.delete_prioridades'
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
        context['title'] = 'Eliminar Prioridad de Trabajo'
        context['entity'] = 'Prioridades de Trabajo'
        context['list_url'] = reverse_lazy('parametros:prioridades_list')
        return context
