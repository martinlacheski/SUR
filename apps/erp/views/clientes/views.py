from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.erp.forms import ClientesForm
from apps.erp.models import Clientes
from apps.mixins import ValidatePermissionRequiredMixin


class ClientesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Clientes
    template_name = 'clientes/list.html'
    permission_required = 'erp.view_clientes'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Clientes.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('erp:clientes_create')
        context['list_url'] = reverse_lazy('erp:clientes_list')
        context['entity'] = 'Clientes'
        return context


class ClientesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'clientes/create.html'
    success_url = reverse_lazy('erp:clientes_list')
    permission_required = 'erp.add_clientes'
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
        context['title'] = 'Crear un Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('erp:clientes_list')
        context['action'] = 'add'
        return context


class ClientesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'clientes/create.html'
    success_url = reverse_lazy('erp:clientes_list')
    permission_required = 'erp.change_clientes'
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
            print(str(e))
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('erp:clientes_list')
        context['action'] = 'edit'
        return context


class ClientesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Clientes
    success_url = reverse_lazy('erp:clientes_list')
    permission_required = 'erp.delete_clientes'
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
        context['title'] = 'Eliminar Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('erp:clientes_list')
        return context
