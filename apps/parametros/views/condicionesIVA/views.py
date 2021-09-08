from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import CondicionesIVAForm
from apps.parametros.models import CondicionesIVA


class CondicionesIVAListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CondicionesIVA
    template_name = 'condicionesIVA/list.html'
    permission_required = 'parametros.view_condicionesiva'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CondicionesIVA.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de condiciones frente al IVA'
        context['create_url'] = reverse_lazy('parametros:condicionesIVA_create')
        context['list_url'] = reverse_lazy('parametros:condicionesIVA_list')
        context['entity'] = 'Condiciones frente al IVA'
        return context


class CondicionesIVACreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = CondicionesIVA
    form_class = CondicionesIVAForm
    template_name = 'condicionesIVA/create.html'
    success_url = reverse_lazy('parametros:condicionesIVA_list')
    permission_required = 'parametros.add_condicionesiva'
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
            print(str(e))
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Condición frente al IVA'
        context['entity'] = 'Condiciones frente al IVA'
        context['list_url'] = reverse_lazy('parametros:condicionesIVA_list')
        context['action'] = 'add'
        return context


class CondicionesIVAUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = CondicionesIVA
    form_class = CondicionesIVAForm
    template_name = 'condicionesIVA/create.html'
    success_url = reverse_lazy('parametros:condicionesIVA_list')
    permission_required = 'parametros.change_condicionesiva'
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
        context['title'] = 'Editar condición frente al IVA'
        context['entity'] = 'Condición frente al IVA'
        context['list_url'] = reverse_lazy('parametros:condicionesIVA_list')
        context['action'] = 'edit'
        return context


class CondicionesIVADeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CondicionesIVA
    success_url = reverse_lazy('parametros:condicionesIVA_list')
    permission_required = 'parametros.delete_condicionesiva'
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
                data['check'] = str(e)
        return JsonResponse(data)

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Condición frente al IVA'
        context['entity'] = 'Condiciones frente al IVA'
        context['list_url'] = reverse_lazy('parametros:condicionesIVA_list')
        return context
