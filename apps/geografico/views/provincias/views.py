from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


from apps.geografico.forms import ProvinciasForm
from apps.geografico.models import Provincias
from apps.mixins import ValidatePermissionRequiredMixin


class ProvinciasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Provincias
    template_name = 'provincias/list.html'
    permission_required = 'geografico.view_provincias'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Provincias.objects.filter(estado=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Provincias'
        context['create_url'] = reverse_lazy('geografico:provincias_create')
        context['list_url'] = reverse_lazy('geografico:provincias_list')
        context['entity'] = 'Provincias'
        return context


class ProvinciasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Provincias
    form_class = ProvinciasForm
    template_name = 'provincias/create.html'
    success_url = reverse_lazy('geografico:provincias_list')
    permission_required = 'geografico.add_provincias'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ProvinciasForm(request.POST)
            data = form.checkAndSave(form, self.url_redirect, request.POST['action'])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Provincia'
        context['entity'] = 'Provincias'
        context['list_url'] = reverse_lazy('geografico:provincias_list')
        context['action'] = 'add'
        return context


class ProvinciasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Provincias
    form_class = ProvinciasForm
    template_name = 'provincias/create.html'
    success_url = reverse_lazy('geografico:provincias_list')
    permission_required = 'geografico.change_provincias'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.POST['action'])
            form = ProvinciasForm(request.POST)
            data = form.checkAndSave(form, self.url_redirect, request.POST['action'])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Provincia'
        context['entity'] = 'Provincias'
        context['list_url'] = reverse_lazy('geografico:provincias_list')
        context['action'] = 'edit'
        return context


class ProvinciasDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Provincias
    success_url = reverse_lazy('geografico:provincias_list')
    permission_required = 'geografico.delete_provincias'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #Captamos el ID y la Accion que viene del Template y realizamos la eliminacion logica
        id = request.POST['pk']
        action = request.POST['action']
        if action == 'delete':
            Provincias.objects.filter(pk=id).update(estado=False)
        return HttpResponseRedirect(self.success_url)


    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Provincia'
        context['entity'] = 'Provincias'
        context['list_url'] = reverse_lazy('geografico:provincias_list')
        return context
