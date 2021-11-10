from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from apps.parametros.forms import EstadoParametrosForm
from apps.parametros.models import EstadoParametros
from apps.mixins import ValidatePermissionRequiredMixin


class EstadoParametrosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = EstadoParametros
    template_name = 'estadoParametros/list.html'
    permission_required = 'parametros.view_estadoparametros'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in EstadoParametros.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estado de Trabajo - Parametros'
        context['create_url'] = reverse_lazy('parametros:estadosParametros_create')
        context['list_url'] = reverse_lazy('parametros:estadosParametros_list')
        context['entity'] = 'Estado de Trabajo - Parametros'
        context['cantParametros'] = EstadoParametros.objects.count()
        return context


class EstadoParametrosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = EstadoParametros
    form_class = EstadoParametrosForm
    template_name = 'estadoParametros/create.html'
    success_url = reverse_lazy('parametros:estadosParametros_list')
    permission_required = 'parametros.add_estadoparametros'
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
        context['title'] = 'Crear Parámetros de Estado de Trabajo'
        context['entity'] = 'Estado de Trabajo - Parametros'
        context['list_url'] = reverse_lazy('parametros:estadosParametros_list')
        context['action'] = 'add'
        return context


class EstadoParametrosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = EstadoParametros
    form_class = EstadoParametrosForm
    template_name = 'estadoParametros/create.html'
    success_url = reverse_lazy('parametros:estadosParametros_list')
    permission_required = 'parametros.change_estadoparametros'
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
        context['title'] = 'Editar Parámetros de Estado de Trabajo'
        context['entity'] = 'Estado de Trabajo - Parametros'
        context['list_url'] = reverse_lazy('parametros:estadosParametros_list')
        context['action'] = 'edit'
        return context
