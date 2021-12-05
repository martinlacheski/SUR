import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, FormView

from apps.parametros.forms import EmpresaForm, UploadBackupForm
from apps.parametros.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from config import settings
import os


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


class BackupView(LoginRequiredMixin, ValidatePermissionRequiredMixin, FormView):
    template_name = 'empresa/backup.html'
    success_url = reverse_lazy('parametros:copia_seguridad')
    permission_required = 'usuarios.add_usuarios'
    url_redirect = success_url
    form_class = UploadBackupForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        # Artificialmente se le da un valor a action en caso de que se trate del upload de un archivo
        try:
            file = request.FILES['file']
            action_artifical = 'restore_backup'
        except Exception as e:
            action_artifical = ''
            pass

        try:
            action = request.POST['action']
            if action == 'create_backup':
                print("imprime")
                # Nombre de la database .json
                database_name = 'backup_SUR_' + datetime.datetime.today().strftime('%d_%m_%Y_%HH_%MM') + '.json'
                # Nombre de la database .zip
                database_name_compress = 'backup_SUR_' + datetime.datetime.today().strftime('%d_%m_%Y_%HH_%MM') + '.zip'
                # Crear la bd .json
                comando_crearBD = 'python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > ' + database_name
                # Comprimirla
                comando_comprimir = 'zip ' + database_name_compress + ' ' + database_name
                # Moverla y borrar el .json
                move = 'mv ' + database_name_compress + ' ' + 'media/backup/' + database_name_compress
                delete = 'rm ' + database_name
                # URL para redirigir al navegador a otra pestaña y así descargar el .zip
                urlBACKUP = settings.MEDIA_URL + 'backup/' + database_name_compress
                # Se crea un dir bakcup únicamente si no existe
                if not os.path.exists('media/backup/'):
                    os.mkdir('media/backup/')
                # Ejecución de comandos
                os.system(comando_crearBD)
                os.system(comando_comprimir)
                os.system(move)
                os.system(delete)
                # Pasamos la url
                data['url'] = urlBACKUP

            # Por el momento no se va a ejecutar
            elif action_artifical == 'restore_backup':
                # Manejo de archivo
                form = UploadBackupForm(request.POST, request.FILES)
                if form.is_valid():
                    # Check de que se haya subido un archivo .zip
                    nombre_archivo = str(request.FILES['file'])
                    if '.zip' in nombre_archivo:
                        nombre_uploaded_backup = 'media/uploaded/uploaded_SUR_' + \
                                                 datetime.datetime.today().strftime('%d_%m_%Y_%HH_%MM') + '.zip'
                        if self.trasladar_archivo(request.FILES['file'], nombre_uploaded_backup):
                            self.restaurar(nombre_uploaded_backup)
                            messages.success(request, 'El sistema se ha reestrablecido.')
                            return render(request, self.template_name, self.get_context_data())
                        else:
                            messages.error(request, 'No se ha podido reestablecer el sistema. Contáctese con el administrador.')
                    else:
                        messages.error(request, 'No se ha cargado un archivo .zip')
                else:
                    messages.error(request, 'No se ha podido reestablecer el sistema. Contáctese con el administrador.')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            pass
            #data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Copias de seguridad del sistema'
        context['create_url'] = reverse_lazy('parametros:copia_seguridad')
        context['list_url'] = reverse_lazy('parametros:copia_seguridad')
        context['home_url'] = reverse_lazy('home:home')
        context['entity'] = 'Copias de seguridad del sistema'
        return context

    # Convierte el archivo en chunks de datos en caso de que el mismo sea muy grande
    def trasladar_archivo(self, archivo, nombre_uploaded_backup):

        # Se crea directorio uploaded si éste no existe
        if not os.path.exists('media/uploaded/'):
            os.mkdir('media/uploaded/')

        try:
            with open(nombre_uploaded_backup, 'wb+') as destination:
                for chunk in archivo.chunks():
                    destination.write(chunk)
                return True
        except Exception as e:
            return False

    # restaura la BD y borra archivos innecesarios
    def restaurar(self, nombre_uploaded_backup):
        # Extrae archivo que subió el user
        cm_extraer = 'unzip ' + nombre_uploaded_backup + ' -d ' + 'media/uploaded/'
        # Restaura la BD desde esa carpeta
        cm_restaurar = 'python manage.py loaddata media/uploaded/*.json'
        # Borra archivos innecesarios
        cm_rm_uploaded_zip = 'rm ' + nombre_uploaded_backup
        cm_rm_uploaded_json = 'rm media/uploaded/*.json'

        # Ejecuta los comandos EN ORDEN
        os.system(cm_extraer)
        os.system(cm_restaurar)
        os.system(cm_rm_uploaded_zip)
        os.system(cm_rm_uploaded_json)
        pass
