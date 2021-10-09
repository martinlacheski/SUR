from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from apps.agenda.forms import *
from apps.agenda.models import tiposEvento
from apps.mixins import ValidatePermissionRequiredMixin

class TiposEventosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = tiposEvento
    template_name = 'gestionTipoEventos/list.html'
    permission_required = 'agenda.view_tiposevento'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in tiposEvento.objects.filter(estado=True):
                    data.append(i.toJSON())
                for tipoEvento in data:
                    tipoEvento['usuariosAsoc'] = self.get_users(tipoEvento['id'])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Eventos'
        context['entity'] = 'Tipos de Eventos'
        context['create_url'] = reverse_lazy('agenda:tiposEventoCreate')
        return context

    def get_users (self, idTipoEvento):
        usuarios = []
        userObj = notificacionUsuarios.objects.filter(tipoEvento=idTipoEvento)
        for users in userObj:
            usuarios.append(" " + users.usuarioNotif.username)
        return usuarios


class TiposEventosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = tiposEvento
    form_class = GestionTiposEventosForm
    template_name = 'gestionTipoEventos/create.html'
    success_url = reverse_lazy('agenda:tiposEventoList')
    permission_required = 'agenda.add_tiposevento'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        datos = {}
        try:
            form = self.get_form()
            print(form.declared_fields)
            data = form.save()
            data['redirect'] = self.url_redirect

            for user in request.POST.getlist('usuarios'):
                notifUsersObj = notificacionUsuarios()
                notifUsersObj.tipoEvento = data['obj']
                notifUsersObj.usuarioNotif = Usuarios.objects.get(pk=user)
                notifUsersObj.save()
            del data['obj']
        except Exception as e:
            datos['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Tipo de Evento'
        context['entity'] = 'Tipos de evento'
        context['list_url'] = reverse_lazy('agenda:tiposEventoList')
        context['action'] = 'add'
        context['usuarios'] = Usuarios.objects.all()
        return context



class TiposEventosEditView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = tiposEvento
    form_class = GestionTiposEventosForm
    template_name = 'gestionTipoEventos/create.html'
    success_url = reverse_lazy('agenda:tiposEventoList')
    permission_required = 'agenda.change_tiposevento'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            form.save()
            data['redirect'] = self.success_url
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Tipo de Evento'
        context['entity'] = 'Tipos de evento'
        context['list_url'] = reverse_lazy('agenda:tiposEventoList')
        context['action'] = 'edit'
        context['usuariosNotif'] = notificacionUsuarios.objects.filter(tipoEvento=self.get_object().id)
        context['usuarios'] = Usuarios.objects.all()
        return context

class TiposEventosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = tiposEvento
    success_url = reverse_lazy('agenda:tiposEventoList')
    permission_required = 'geografico.delete_tiposevento'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        id = request.POST['pk']
        action = request.POST['action']
        if action == 'delete':
            try:
                N_users = notificacionUsuarios.objects.filter(tipoEvento=self.object.id)
                for n in N_users:
                    print(n)
                tipoEV = tiposEvento.objects.get(pk=self.object.id)
                tipoEV.estado = False
                tipoEV.save()
                data['redirect'] = self.url_redirect
                data['check'] = 'ok'
            except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Tipo de Evento'
        context['entity'] = 'Tipos de evento'
        context['list_url'] = reverse_lazy('agenda:tiposEventoList')
        return context