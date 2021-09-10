from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.usuarios.forms import UsuariosForm, UsuariosProfileForm
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
                data = form.save()
                data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado ninguna opción'
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
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    # Convertimos a MAYUSCULAS los siguientes campos
                    self.object.first_name = form.cleaned_data['first_name'].upper()
                    self.object.last_name = form.cleaned_data['last_name'].upper()
                    self.object.direccion = form.cleaned_data['direccion'].upper()
                data = form.save()
                data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado ninguna opción'
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


class UsuariosPerfilView(LoginRequiredMixin, UpdateView):
    model = Usuarios
    form_class = UsuariosProfileForm
    template_name = 'usuarios/profile.html'
    success_url = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                data['redirect'] = self.success_url
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UsuariosChangePasswordView(LoginRequiredMixin, FormView):
    model = Usuarios
    form_class = PasswordChangeForm
    template_name = 'usuarios/change_password.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    data['redirect'] = self.success_url
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Contraseña'
        context['entity'] = 'Contraseña'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
