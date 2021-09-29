from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import CondicionesPagoForm
from apps.parametros.models import CondicionesPago


class CondicionesPagoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CondicionesPago
    template_name = 'condicionesPago/list.html'
    permission_required = 'parametros.view_condicionespago'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CondicionesPago.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de condiciones de Pago'
        context['create_url'] = reverse_lazy('parametros:condicionesPago_create')
        context['list_url'] = reverse_lazy('parametros:condicionesPago_list')
        context['entity'] = 'Condiciones de Pago'
        return context


class CondicionesPagoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = CondicionesPago
    form_class = CondicionesPagoForm
    template_name = 'condicionesPago/create.html'
    success_url = reverse_lazy('parametros:condicionesPago_list')
    permission_required = 'parametros.add_condicionespago'
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
        context['title'] = 'Crear una Condición de Pago'
        context['entity'] = 'Condiciones de Pago'
        context['list_url'] = reverse_lazy('parametros:condicionesPago_list')
        context['action'] = 'add'
        return context


class CondicionesPagoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = CondicionesPago
    form_class = CondicionesPagoForm
    template_name = 'condicionesPago/create.html'
    success_url = reverse_lazy('parametros:condicionesPago_list')
    permission_required = 'parametros.change_condicionespago'
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
        context['title'] = 'Editar condición de Pago'
        context['entity'] = 'Condiciones de Pago'
        context['list_url'] = reverse_lazy('parametros:condicionesPago_list')
        context['action'] = 'edit'
        return context


class CondicionesPagoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CondicionesPago
    success_url = reverse_lazy('parametros:condicionesPago_list')
    permission_required = 'parametros.delete_condicionespago'
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
        context['title'] = 'Eliminar Condición de Pago'
        context['entity'] = 'Condiciones de Pago'
        context['list_url'] = reverse_lazy('parametros:condicionesPago_list')
        return context
