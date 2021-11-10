from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from apps.mixins import ValidatePermissionRequiredMixin
from apps.bot_telegram.models import *
from apps.bot_telegram.forms import *

class notifIncidentesUsersListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = notifIncidentesUsuarios
    template_name = 'usersNotifIncidencias/list.html'
    permission_required = 'bot.view_notifincidentesusuarios'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # Solamente mostramos usuarios que tengan chatID
                for i in notifIncidentesUsuarios.objects.all():
                    data.append(i.toJSON())

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios a notificar'
        context['entity'] = 'Users a notificar'
        context['create_url'] = reverse_lazy('bot:notifIncidenCreate')
        return context

class notifIncidentesUsersCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = notifIncidentesUsuarios
    form_class = gestionNotifIncidenciasForm
    template_name = 'usersNotifIncidencias/create.html'
    success_url = reverse_lazy('bot:notifIncidenList')
    permission_required = 'bot.add_notifincidentesusuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
            data['redirect'] = self.url_redirect

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un Usuario a ser Notificado'
        context['entity'] = 'Users a notificar'
        context['list_url'] = reverse_lazy('bot:notifIncidenList')
        context['action'] = 'add'
        return context


class notifIncidentesUsersEditView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = notifIncidentesUsuarios
    form_class = gestionNotifIncidenciasForm
    template_name = 'usersNotifIncidencias/create.html'
    success_url = reverse_lazy('bot:notifIncidenList')
    permission_required = 'bot.change_notifincidentesusuarios'
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
        context['title'] = 'Modificar un Usuario a ser Notificado'
        context['entity'] = 'Users a notificar'
        context['list_url'] = reverse_lazy('bot:notifIncidenList')
        context['action'] = 'edit'
        return context

class notifIncidentesUsersDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = notifIncidentesUsuarios
    success_url = reverse_lazy('bot:notifIncidenList')
    permission_required = 'bot.delete_notifincidentesusuarios'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
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
        context['title'] = 'Eliminar un Usuario a ser notificado'
        context['entity'] = 'Users a notificar'
        context['list_url'] = reverse_lazy('bot:notifIncidenList')
        return context
