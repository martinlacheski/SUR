from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.forms import model_to_dict

from apps.usuarios.forms import GruposUsuariosForm


class GruposUsuariosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Group
    template_name = 'gruposUsuarios/list.html'
    permission_required = 'usuarios.view_group'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        data_list = []
        action = request.POST['action']
        if action == 'searchdata':
            for i in Group.objects.all():
                i = model_to_dict(i)
                del i['permissions']
                data_list.append(i)
        else:
            data['error'] = 'Ha ocurrido un error'
        return JsonResponse(data_list, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Grupos de Usuarios'
        context['create_url'] = reverse_lazy('usuarios:grupos_usuarios_create')
        #context['list_url'] = reverse_lazy('usuarios:tipos_usuarios_list')
        context['entity'] = 'Grupos de Usuarios'
        return context

class GruposUsuariosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Group
    form_class = GruposUsuariosForm
    template_name = 'gruposUsuarios/create.html'
    success_url = reverse_lazy('usuarios:grupos_usuarios_list')
    permission_required = 'usuarios.add_group'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            grupo = Group.objects.get(name=request.POST['name'].upper())
            data['error'] = "Ya existe un grupo con este nombre"
        except ObjectDoesNotExist:
            # Creación de objeto grupo
            nuevoGrupo = Group()
            nuevoGrupo.name = request.POST['name'].upper()

            # Importante guardar únicamente con su nombre.
            nuevoGrupo.save()

            # Una vez guardado, le agregamos sus permisos.
            for p in request.POST.getlist('permisos'):
                p_Obj = Permission.objects.get(codename=p)
                nuevoGrupo.permissions.add(p_Obj)
            nuevoGrupo.save()
            data['redirect'] = self.url_redirect
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Grupo'
        context['entity'] = 'Grupos de Usuarios'
        context['list_url'] = reverse_lazy('usuarios:grupos_usuarios_list')
        context['permisos'] = Permission.objects.all()
        context['action'] = 'add'
        return context

class GruposUsuariosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Group
    form_class = GruposUsuariosForm
    template_name = 'gruposUsuarios/create.html'
    success_url = reverse_lazy('usuarios:grupos_usuarios_list')
    permission_required = 'usuarios.change_group'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                try:
                    grupo = Group.objects.get(name=request.POST['name'].upper())
                    data['error'] = "Ya existe un grupo con este nombre"
                except ObjectDoesNotExist:
                    # Garda grupo SOLAMENTE con su nombre.
                    self.object.name = request.POST['name']
                    self.object.save()

                    # Elimina todos sus permisos
                    self.object.permissions.clear()

                    # Los crea nuevamente.
                    for p in request.POST.getlist('permisos'):
                        p_Obj = Permission.objects.get(codename=p)
                        self.object.permissions.add(p_Obj)
                    self.object.save()
                    data['redirect'] = self.url_redirect
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Grupo de Usuario'
        context['entity'] = 'Grupos de Usuarios'
        context['list_url'] = reverse_lazy('usuarios:grupos_usuarios_list')
        context['action'] = 'edit'
        context['permisosDeUsuario'] = self.object.permissions.all()
        context['permisos'] = Permission.objects.all()
        return context

class GruposUsuariosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('usuarios:grupos_usuarios_list')
    permission_required = 'usuarios.delete_group'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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

