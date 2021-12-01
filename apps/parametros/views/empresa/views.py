from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, TemplateView

from apps.parametros.forms import EmpresaForm
from apps.parametros.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from config import settings


class EmpresaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Empresa
    template_name = 'empresa/list.html'
    permission_required = 'parametros.view_empresa'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Empresa.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Empresas'
        context['create_url'] = reverse_lazy('parametros:empresa_create')
        context['list_url'] = reverse_lazy('parametros:empresa_list')
        context['entity'] = 'Empresa'
        context['cantEmpresa'] = Empresa.objects.count()
        return context


class EmpresaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/create.html'
    success_url = reverse_lazy('parametros:empresa_list')
    permission_required = 'parametros.add_empresa'
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
        context['title'] = 'Datos Empresa'
        context['entity'] = 'Empresa'
        context['list_url'] = reverse_lazy('parametros:empresa_list')
        context['action'] = 'add'
        context['cantEmpresa'] = Empresa.objects.count()
        return context


class EmpresaView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/view.html'
    success_url = reverse_lazy('parametros:empresa_list')
    permission_required = 'parametros.view_empresa'
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
        context['title'] = 'Ver Empresa'
        context['entity'] = 'Empresa'
        context['list_url'] = reverse_lazy('parametros:empresa_list')
        context['action'] = 'edit'
        return context


class EmpresaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/create.html'
    success_url = reverse_lazy('parametros:empresa_list')
    permission_required = 'parametros.change_empresa'
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
        context['title'] = 'Editar Empresa'
        context['entity'] = 'Empresa'
        context['list_url'] = reverse_lazy('parametros:empresa_list')
        context['action'] = 'edit'
        return context

class BackupView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'empresa/backup.html'
    success_url = reverse_lazy('home:home')
    permission_required = 'usuarios.add_usuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create_backup':
                # Asignamos la ruta donde se guarda el PDF
                urlWrite = settings.MEDIA_ROOT + 'backup_SUR.json'
                # Asignamos la ruta donde se visualiza el PDF
                urlBACKUP = settings.MEDIA_URL + 'backup_SUR.json'
                # Creamos el BACKUP ACA
                data['url'] = urlBACKUP
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Copias de seguridad del sistema'
        context['create_url'] = reverse_lazy('parametros:copia_seguridad')
        context['list_url'] = reverse_lazy('home:home')
        context['entity'] = 'Copias de seguridad del sistema'
        return context