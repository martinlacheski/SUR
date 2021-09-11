from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.erp.forms import ServiciosForm
from apps.erp.models import Servicios
from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import TiposIVA


class ServiciosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Servicios
    template_name = 'servicios/list.html'
    permission_required = 'erp.view_servicios'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Servicios.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicios'
        context['create_url'] = reverse_lazy('erp:servicios_create')
        context['list_url'] = reverse_lazy('erp:servicios_list')
        context['entity'] = 'Servicios'
        return context


class ServiciosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Servicios
    form_class = ServiciosForm
    template_name = 'servicios/create.html'
    success_url = reverse_lazy('erp:servicios_list')
    permission_required = 'erp.add_servicios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            elif action == 'add':
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
        context['title'] = 'Crear un Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('erp:servicios_list')
        context['action'] = 'add'
        return context


class ServiciosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Servicios
    form_class = ServiciosForm
    template_name = 'servicios/create.html'
    success_url = reverse_lazy('erp:servicios_list')
    permission_required = 'erp.change_servicios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_iva':
                iva = TiposIVA.objects.get(id=request.POST['pk'])
                data['iva'] = iva.iva
            elif action == 'edit':
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
        context['title'] = 'Editar Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('erp:servicios_list')
        context['action'] = 'edit'
        return context


class ServiciosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Servicios
    success_url = reverse_lazy('erp:servicios_list')
    permission_required = 'erp.delete_servicios'
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
        context['title'] = 'Eliminar Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('erp:servicios_list')
        return context
