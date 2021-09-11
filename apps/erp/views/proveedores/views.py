from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.erp.forms import ProveedoresForm
from apps.erp.models import Proveedores
from apps.mixins import ValidatePermissionRequiredMixin


class ProveedoresListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Proveedores
    template_name = 'proveedores/list.html'
    permission_required = 'erp.view_proveedores'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proveedores.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('erp:proveedores_create')
        context['list_url'] = reverse_lazy('erp:proveedores_list')
        context['entity'] = 'Proveedores'
        return context


class ProveedoresCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Proveedores
    form_class = ProveedoresForm
    template_name = 'proveedores/create.html'
    success_url = reverse_lazy('erp:proveedores_list')
    permission_required = 'erp.add_proveedores'
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
        context['title'] = 'Crear un Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = reverse_lazy('erp:proveedores_list')
        context['action'] = 'add'
        return context


class ProveedoresUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Proveedores
    form_class = ProveedoresForm
    template_name = 'proveedores/create.html'
    success_url = reverse_lazy('erp:proveedores_list')
    permission_required = 'erp.change_proveedores'
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
        context['title'] = 'Editar Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = reverse_lazy('erp:proveedores_list')
        context['action'] = 'edit'
        return context


class ProveedoresDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Proveedores
    success_url = reverse_lazy('erp:proveedores_list')
    permission_required = 'erp.delete_proveedores'
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
        context['title'] = 'Eliminar Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = reverse_lazy('erp:proveedores_list')
        return context
