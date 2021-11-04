from django.apps import AppConfig
from simple_history.signals import pre_create_historical_record




class ErpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.erp'
    verbose_name = "Módulo ERP"


# Creamos la configuracion para agregar el campo extra en el detalle de history
class HistoryVentasConfig(AppConfig):
    def ready(self):
        from apps.erp.models import DetalleProductosVenta, DetalleServiciosVenta
        from apps.erp.models import add_history_venta_history_id
        pre_create_historical_record.connect(add_history_venta_history_id, sender=DetalleProductosVenta)
        pre_create_historical_record.connect(add_history_venta_history_id, sender=DetalleServiciosVenta)
