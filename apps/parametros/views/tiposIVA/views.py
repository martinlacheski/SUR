from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import TiposIVAForm
from apps.parametros.models import TiposIVA


class TiposIVAListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TiposIVA
    template_name = 'tiposIVA/list.html'
    permission_required = 'parametros.view_tiposiva'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TiposIVA.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de IVA'
        context['create_url'] = reverse_lazy('parametros:tiposIVA_create')
        context['list_url'] = reverse_lazy('parametros:tiposIVA_list')
        context['entity'] = 'Tipos de IVA'
        return context


class TiposIVACreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TiposIVA
    form_class = TiposIVAForm
    template_name = 'tiposIVA/create.html'
    success_url = reverse_lazy('parametros:tiposIVA_list')
    permission_required = 'parametros.add_tiposiva'
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
        context['title'] = 'Crear un Tipo de IVA'
        context['entity'] = 'Tipos de IVA'
        context['list_url'] = reverse_lazy('parametros:tiposIVA_list')
        context['action'] = 'add'
        return context


class TiposIVAUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TiposIVA
    form_class = TiposIVAForm
    template_name = 'tiposIVA/create.html'
    success_url = reverse_lazy('parametros:tiposIVA_list')
    permission_required = 'parametros.change_tiposiva'
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
        context['title'] = 'Editar Tipo de IVA'
        context['entity'] = 'Tipos de IVA'
        context['list_url'] = reverse_lazy('parametros:tiposIVA_list')
        context['action'] = 'edit'
        return context


class TiposIVADeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TiposIVA
    success_url = reverse_lazy('parametros:tiposIVA_list')
    permission_required = 'parametros.delete_tiposiva'
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
        context['title'] = 'Eliminar Tipo de IVA'
        context['entity'] = 'Tipos de IVA'
        context['list_url'] = reverse_lazy('parametros:tiposIVA_list')
        return context
