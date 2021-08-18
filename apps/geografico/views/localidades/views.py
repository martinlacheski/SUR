from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from apps.geografico.forms import LocalidadesForm
from apps.geografico.models import Localidades, Provincias
from apps.mixins import ValidatePermissionRequiredMixin


class LocalidadesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Localidades
    template_name = 'localidades/list.html'
    permission_required = 'geografico.view_localidades'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Localidades.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Localidades'
        context['create_url'] = reverse_lazy('geografico:localidades_create')
        context['list_url'] = reverse_lazy('geografico:localidades_list')
        context['entity'] = 'Localidades'
        return context


class LocalidadesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Localidades
    form_class = LocalidadesForm
    template_name = 'localidades/create.html'
    success_url = reverse_lazy('geografico:localidades_list')
    permission_required = 'geografico.add_localidades'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # Realizamos la busqueda de Provincias de un X pais y cargamos el Select de provincias
            if action == 'search_provincias':
                data = [{'id': '', 'text': '---------'}]
                for i in Provincias.objects.filter(pais_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})

            # Ya sea action 'edit' o action 'add'
            else:
                form = self.get_form()
                data = form.checkAndSave(form, self.url_redirect, request.POST['action'])
        except Exception as e:
            data['error'] = str(e)
        # Se debe especificar en el return por la devolucion de datos Serializados
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Localidad'
        context['entity'] = 'Localidades'
        context['list_url'] = reverse_lazy('geografico:localidades_list')
        context['action'] = 'add'
        return context


class LocalidadesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Localidades
    form_class = LocalidadesForm
    template_name = 'localidades/create.html'
    success_url = reverse_lazy('geografico:localidades_list')
    permission_required = 'geografico.change_localidades'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # Realizamos la busqueda de Provincias de un X pais y cargamos el Select de provincias
            if action == 'search_provincias':
                data = [{'id': '', 'text': '---------'}]
                for i in Provincias.objects.filter(pais_id=request.POST['pk']):
                    data.append({'id': i.id, 'text': i.nombre})
            else:
                form = self.get_form()
                data = form.checkAndSave(form, self.url_redirect, request.POST['action'])
        except Exception as e:
            data['error'] = str(e)
        # Se debe especificar en el return por la devolucion de datos Serializados
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Localidad'
        context['entity'] = 'Localidades'
        context['list_url'] = reverse_lazy('geografico:localidades_list')
        context['action'] = 'edit'
        return context


class LocalidadesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Localidades
    success_url = reverse_lazy('geografico:localidades_list')
    permission_required = 'geografico.delete_localidades'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Captamos el ID y la Accion que viene del Template y realizamos la eliminacion logica
        id = request.POST['pk']
        action = request.POST['action']
        if action == 'delete':
            self.object.delete()
        return HttpResponseRedirect(self.success_url)

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Localidad'
        context['entity'] = 'Localidades'
        context['list_url'] = reverse_lazy('geografico:localidades_list')
        return context
