from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from apps.agenda.models import *
from apps.agenda.forms import *
from apps.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy


class DashboardAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    template_name = 'gestionEventos/list.html'
    model = eventosAgenda
    form_class = GestionEventosForm
    permission_required = 'agenda.add_tiposevento'
    success_url = reverse_lazy('agenda:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
            #data = form.save()
        except Exception as e:
            data['error'] = str(e)
        #return JsonResponse(data, safe=False)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = eventosAgenda.objects.all()
        return context


class UpdateEventosAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = eventosAgenda
    form_class = GestionEventosForm
    success_url = reverse_lazy('agenda:dashboard')
    permission_required = 'agenda.change_tiposevento'
    template_name = 'gestionEventos/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['entity'] = 'Países'
        context['update_url'] = self.success_url
        context['action'] = 'edit'
        return context


# class DeleteEventoAgenda(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
#     model = eventosAgenda
#     form_class = GestionEventosForm
#     succes_url = reverse_lazy('agenda:dashboard')
#
#     def post(self, request, *args, **kwargs):
#         id = request.POST['pk']
#         action = request.POST['action']


class PaisesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Paises
    form_class = PaisesForm
    template_name = 'paises/create.html'
    success_url = reverse_lazy('geografico:paises_list')
    permission_required = 'geografico.change_paises'
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
        context['title'] = 'Editar País'
        context['entity'] = 'Países'
        context['list_url'] = reverse_lazy('geografico:paises_list')
        context['action'] = 'edit'
        return context

