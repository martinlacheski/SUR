from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from apps.agenda.models import *
from apps.agenda.forms import *
from apps.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from apps.agenda.jobs import scheduler_eventos


class DashboardAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    template_name = 'gestionEventos/list.html'
    model = eventosAgenda
    form_class = GestionEventosForm
    permission_required = 'agenda.add_eventosagenda'
    success_url = reverse_lazy('agenda:dashboard')

    def post(self, request, *args, **kwargs):
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
                #scheduler_eventos()
            else:
                print(form.errors)
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = eventosAgenda.objects.all()
        context['update_url'] = 'agenda/updateEvento/'
        context['delete_url'] = '/agenda/deleteEvento/'
        context['action'] = 'add'
        return context




class UpdateEventosAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = eventosAgenda
    form_class = GestionEventosForm
    success_url = reverse_lazy('agenda:dashboard')
    permission_required = 'agenda.change_eventosagenda'
    template_name = 'gestionEventos/list.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = eventosAgenda.objects.all()
        context['update_url'] = 'agenda/updateEvento/'
        context['action'] = 'edit'
        context['delete_url'] = '/agenda/deleteEvento/'
        return context

class DeleteEventosAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = eventosAgenda
    success_url = reverse_lazy('agenda:dashboard')
    permission_required = 'agenda.delete_eventosagenda'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

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