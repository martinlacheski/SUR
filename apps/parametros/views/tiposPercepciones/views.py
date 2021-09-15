from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import TiposPercepcionesForm
from apps.parametros.models import TiposPercepciones


class TiposPercepcionesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TiposPercepciones
    template_name = 'tiposPercepciones/list.html'
    permission_required = 'parametros.view_tipospercepciones'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TiposPercepciones.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Percepciones'
        context['create_url'] = reverse_lazy('parametros:tiposPercepciones_create')
        context['list_url'] = reverse_lazy('parametros:tiposPercepciones_list')
        context['entity'] = 'Tipos de Percepciones'
        return context


class TiposPercepcionesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TiposPercepciones
    form_class = TiposPercepcionesForm
    template_name = 'tiposPercepciones/create.html'
    success_url = reverse_lazy('parametros:tiposPercepciones_list')
    permission_required = 'parametros.add_tipospercepciones'
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
        context['title'] = 'Crear un Tipo de Percepción'
        context['entity'] = 'Tipos de Percepciones'
        context['list_url'] = reverse_lazy('parametros:tiposPercepciones_list')
        context['action'] = 'add'
        return context


class TiposPercepcionesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TiposPercepciones
    form_class = TiposPercepcionesForm
    template_name = 'tiposPercepciones/create.html'
    success_url = reverse_lazy('parametros:tiposPercepciones_list')
    permission_required = 'parametros.change_tipospercepciones'
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
        context['title'] = 'Editar Tipo de Percepción'
        context['entity'] = 'Tipos de Percepciones'
        context['list_url'] = reverse_lazy('parametros:tiposPercepciones_list')
        context['action'] = 'edit'
        return context


class TiposPercepcionesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TiposPercepciones
    success_url = reverse_lazy('parametros:tiposPercepciones_list')
    permission_required = 'parametros.delete_tipospercepciones'
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
        context['title'] = 'Eliminar Tipo de Percepción'
        context['entity'] = 'Tipos de Percepciones'
        context['list_url'] = reverse_lazy('parametros:tiposPercepciones_list')
        return context
