from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.geografico.forms import PaisesForm
from apps.geografico.models import Paises
from apps.mixins import ValidatePermissionRequiredMixin


class PaisesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Paises
    template_name = 'paises/list.html'
    redirect_template = ''
    permission_required = 'geografico.view_paises'
    success_url = reverse_lazy('agenda:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission_required):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("No tenés permiso para realizar esta acción")

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Paises.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Países'
        context['create_url'] = reverse_lazy('geografico:paises_create')
        context['list_url'] = reverse_lazy('geografico:paises_list')
        context['entity'] = 'Paises'
        return context


class PaisesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView, AccessMixin):
    model = Paises
    form_class = PaisesForm
    template_name = 'paises/create.html'
    success_url = reverse_lazy('geografico:paises_list')
    permission_required = 'geografico.add_paises'
    url_redirect = success_url
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = {}
            try:
                action = request.POST['action']
                if action == 'add':
                    form = self.get_form()
                    data = form.save()
                    data['redirect'] = self.url_redirect
                else:
                    data['error'] = 'No ha ingresado a ninguna opción'
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data)
        except PermissionDenied:
            print("no tiene permiso")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un País'
        context['entity'] = 'Paises'
        context['list_url'] = reverse_lazy('geografico:paises_list')
        context['action'] = 'add'
        return context


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
        context['title'] = 'Editar País'
        context['entity'] = 'Países'
        context['list_url'] = reverse_lazy('geografico:paises_list')
        context['action'] = 'edit'
        return context


class PaisesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Paises
    success_url = reverse_lazy('geografico:paises_list')
    permission_required = 'geografico.delete_paises'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Captamos el ID y la Accion que viene del Template y realizamos la eliminacion logica
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
        context['title'] = 'Eliminar País'
        context['entity'] = 'Países'
        context['list_url'] = reverse_lazy('geografico:paises_list')
        return context
