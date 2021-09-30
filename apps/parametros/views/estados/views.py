import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.forms import EstadosForm
from apps.parametros.models import Estados


class EstadosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Estados
    template_name = 'estados/list.html'
    permission_required = 'parametros.view_estados'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Estados.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Estados de Trabajo'
        context['create_url'] = reverse_lazy('parametros:estados_create')
        context['list_url'] = reverse_lazy('parametros:estados_list')
        context['order_url'] = reverse_lazy('parametros:estados_order')
        context['entity'] = 'Estados de Trabajo'
        return context


class EstadosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Estados
    form_class = EstadosForm
    template_name = 'estados/create.html'
    success_url = reverse_lazy('parametros:estados_list')
    permission_required = 'parametros.add_estados'
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
        context['title'] = 'Crear un Estado de Trabajo'
        context['entity'] = 'Estados de Trabajo'
        context['list_url'] = reverse_lazy('parametros:estados_list')
        context['action'] = 'add'
        return context


class EstadosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Estados
    form_class = EstadosForm
    template_name = 'estados/create.html'
    success_url = reverse_lazy('parametros:estados_list')
    permission_required = 'parametros.change_estados'
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
        context['title'] = 'Editar Estado de Trabajo'
        context['entity'] = 'Estados de Trabajo'
        context['list_url'] = reverse_lazy('parametros:estados_list')
        context['action'] = 'edit'
        return context


class EstadosOrderView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Estados
    form_class = EstadosForm
    template_name = 'estados/order.html'
    success_url = reverse_lazy('parametros:estados_list')
    permission_required = 'parametros.change_estados'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Estados.objects.all():
                    data.append(i.toJSON())
            elif action == 'order':
                # Asignamos a una Variable el orden de los estados que viene del Formulario
                ordenEstadosTrabajo = json.loads(request.POST['orderEstados'])
                pos = 1
                for i in ordenEstadosTrabajo:
                    # Buscamos el Estado de Trabajo para actualizar la posicion
                    with transaction.atomic():
                        estado = Estados.objects.get(id=i)
                        estado.orden = pos
                        estado.save()
                    pos+=1
                data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Orden de Estados de Trabajo'
        context['entity'] = 'Estados de Trabajo'
        context['list_url'] = reverse_lazy('parametros:estados_list')
        context['estados'] = Estados.objects.all()
        context['action'] = 'order'
        return context


class EstadosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Estados
    success_url = reverse_lazy('parametros:estados_list')
    permission_required = 'parametros.delete_estados'
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
        context['title'] = 'Eliminar Estado de Trabajo'
        context['entity'] = 'Estados de Trabajo'
        context['list_url'] = reverse_lazy('parametros:estados_list')
        return context
