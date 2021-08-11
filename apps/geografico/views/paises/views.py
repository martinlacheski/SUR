from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from apps.geografico.forms import PaisesForm
from apps.geografico.models import Paises
from apps.mixins import ValidatePermissionRequiredMixin


class PaisesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Paises
    template_name = 'paises/list.html'
    permission_required = 'geografico.view_paises'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Paises.objects.filter(estado=True):
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


class PaisesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Paises
    form_class = PaisesForm
    template_name = 'paises/create.html'
    success_url = reverse_lazy('geografico:paises_list')
    permission_required = 'geografico.add_paises'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            # agregar action check
            if action == 'check':
                value = request.POST['value']
                print(value)
                data['check'] = True
            elif action == 'add':
                form = self.get_form()
                # Buscamos pais
                if (form.is_valid()):
                    # Si existe, alteramos su estado. Si no existe, guardamos
                    try:
                        pais = Paises.objects.get(nombre=form.cleaned_data['nombre'].upper())
                        Paises.objects.filter(pk=pais.id).update(estado=True)
                    except Exception as e:
                        # print(str(e))
                        data = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

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
                return HttpResponseRedirect(self.success_url)
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


class PaisesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
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
            Paises.objects.filter(pk=id).update(estado=False)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar País'
        context['entity'] = 'Países'
        context['list_url'] = reverse_lazy('geografico:paises_list')
        return context
