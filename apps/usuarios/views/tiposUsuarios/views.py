from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


from apps.mixins import ValidatePermissionRequiredMixin
from apps.usuarios.forms import TiposUsuariosForm
from apps.usuarios.models import TiposUsuarios


class TiposUsuariosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TiposUsuarios
    template_name = 'tiposUsuarios/list.html'
    permission_required = 'usuarios.view_tiposusuarios'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TiposUsuarios.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Usuarios'
        context['create_url'] = reverse_lazy('usuarios:tipos_usuarios_create')
        context['list_url'] = reverse_lazy('usuarios:tipos_usuarios_list')
        context['entity'] = 'Tipos de Usuarios'
        return context


class TiposUsuariosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TiposUsuarios
    form_class = TiposUsuariosForm
    template_name = 'tiposUsuarios/create.html'
    success_url = reverse_lazy('usuarios:tipos_usuarios_list')
    permission_required = 'usuarios.add_tiposusuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.checkAndSave(form, self.url_redirect, request.POST['action'])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Tipo de Usuario'
        context['entity'] = 'Tipos de Usuarios'
        context['list_url'] = reverse_lazy('usuarios:tipos_usuarios_list')
        context['action'] = 'add'
        return context


class TiposUsuariosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TiposUsuarios
    form_class = TiposUsuariosForm
    template_name = 'tiposUsuarios/create.html'
    success_url = reverse_lazy('usuarios:tipos_usuarios_list')
    permission_required = 'usuarios.change_tiposusuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.checkAndSave(form, self.url_redirect, request.POST['action'])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Usuario'
        context['entity'] = 'Tipos de Usuarios'
        context['list_url'] = reverse_lazy('usuarios:tipos_usuarios_list')
        context['action'] = 'edit'
        return context


class TiposUsuariosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TiposUsuarios
    success_url = reverse_lazy('usuarios:tipos_usuarios_list')
    permission_required = 'usuarios.delete_tiposusuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Captamos el ID y la Accion que viene del Template
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
        context['title'] = 'Eliminar Tipo de Usuario'
        context['entity'] = 'Tipos de Usuarios'
        context['list_url'] = reverse_lazy('usuarios:tipos_usuarios_list')
        return context
