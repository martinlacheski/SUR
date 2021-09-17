from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import MediosPagoForm
from apps.parametros.models import MediosPago


class MediosPagoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = MediosPago
    template_name = 'mediosPago/list.html'
    permission_required = 'parametros.view_mediospago'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in MediosPago.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Medios de Pago'
        context['create_url'] = reverse_lazy('parametros:mediosPago_create')
        context['list_url'] = reverse_lazy('parametros:mediosPago_list')
        context['entity'] = 'Medios de Pago'
        return context


class MediosPagoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = MediosPago
    form_class = MediosPagoForm
    template_name = 'mediosPago/create.html'
    success_url = reverse_lazy('parametros:mediosPago_list')
    permission_required = 'parametros.add_mediospago'
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
        context['title'] = 'Crear un Medio de Pago'
        context['entity'] = 'Medios de Pago'
        context['list_url'] = reverse_lazy('parametros:mediosPago_list')
        context['action'] = 'add'
        return context


class MediosPagoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = MediosPago
    form_class = MediosPagoForm
    template_name = 'mediosPago/create.html'
    success_url = reverse_lazy('parametros:mediosPago_list')
    permission_required = 'parametros.change_mediospago'
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
        context['title'] = 'Editar Medio de Pago'
        context['entity'] = 'Medios de Pago'
        context['list_url'] = reverse_lazy('parametros:mediosPago_list')
        context['action'] = 'edit'
        return context


class MediosPagoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = MediosPago
    success_url = reverse_lazy('parametros:mediosPago_list')
    permission_required = 'parametros.delete_mediospago'
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
        context['title'] = 'Eliminar Medio de Pago'
        context['entity'] = 'Medios de Pago'
        context['list_url'] = reverse_lazy('parametros:mediosPago_list')
        return context
