from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.usuarios.forms import UsuariosForm
from apps.usuarios.models import Usuarios


class UsuariosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Usuarios
    template_name = 'usuarios/list.html'
    permission_required = 'usuarios.view_usuarios'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Usuarios.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['create_url'] = reverse_lazy('usuarios:usuarios_create')
        context['list_url'] = reverse_lazy('usuarios:usuarios_list')
        context['entity'] = 'Usuarios'
        return context

class UsuariosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'usuarios/create.html'
    success_url = reverse_lazy('usuarios:usuarios_list')
    permission_required = 'usuarios.add_usuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    try:
                        # Si existe el objeto que se quiere guardar/editar y está activo, error.
                        usuario = Usuarios.objects.get(username=form.cleaned_data['username'].upper())
                        data['check'] = True
                    except Exception as e:
                        data['check'] = 'Registrar'
                        data['redirect'] = reverse_lazy('usuarios:usuarios_list')
                        print(form.cleaned_data['imagen'])
                        form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('usuarios:usuarios_list')
        context['action'] = 'add'
        return context

class UsuariosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'usuarios/create.html'
    success_url = reverse_lazy('usuarios:usuarios_list')
    permission_required = 'usuarios.change_usuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.FILES)
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    try:
                        # Si existe el objeto que se quiere guardar/editar y está activo, error.
                        usuario = Usuarios.objects.get(username=form.cleaned_data['username'].upper())
                        data['check'] = True
                    except Exception as e:
                        data['check'] = 'Registrar'
                        data['redirect'] = reverse_lazy('usuarios:usuarios_list')
                        self.object.first_name = form.cleaned_data['first_name'].upper()
                        self.object.last_name = form.cleaned_data['last_name'].upper()
                        self.object.direccion = form.cleaned_data['direccion'].upper()
                        print(form.cleaned_data['imagen'])
                        form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('usuarios:usuarios_list')
        context['action'] = 'edit'
        return context

class UsuariosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Usuarios
    success_url = reverse_lazy('usuarios:usuarios_list')
    permission_required = 'usuarios.delete_usuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['redirect'] = self.url_redirect
            data['check'] = 'ok'
        except Exception as e:
            data['check'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('usuarios:usuarios_list')
        return context
