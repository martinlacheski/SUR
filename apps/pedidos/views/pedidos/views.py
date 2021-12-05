import os

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from apps.mixins import ValidatePermissionRequiredMixin
from apps.parametros.models import Empresa
from apps.pedidos.models import Pedidos, DetallePedido
from config import settings

from weasyprint import HTML, CSS


class PedidosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Pedidos
    template_name = 'pedidos/list.html'
    permission_required = 'pedidos.view_pedidos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Pedidos.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_detalle_pedido':
                data = []
                for i in DetallePedido.objects.filter(pedido_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pedidos'
        context['create_url'] = reverse_lazy('pedidos:pedidos_create')
        context['list_url'] = reverse_lazy('pedidos:pedidos_list')
        context['entity'] = 'Pedidos'
        return context


class PedidosPdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'pedidos.view_pedidos'

    def get(self, request, *args, **kwargs):
        try:
            # Traemos la empresa para obtener los valores
            empresa = Empresa.objects.get(pk=Empresa.objects.all().last().id)
            # Utilizamos el template para generar el PDF
            template = get_template('pedidos/pdf.html')
            context = {
                'pedido': Pedidos.objects.get(pk=self.kwargs['pk']),
                'empresa': {'nombre': empresa.razonSocial, 'cuit': empresa.cuit, 'direccion': empresa.direccion,
                            'localidad': empresa.localidad.get_full_name(), 'imagen': empresa.imagen},
            }
            # Generamos el render del contexto
            html = template.render(context)
            # Asignamos la ruta del CSS de BOOTSTRAP
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            # Creamos el PDF
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('pedidos:pedidos_list'))
