from django.forms import ModelForm, TextInput, Select

from apps.bot_telegram.models import *


class gestionNotifIncidenciasForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['nombre'].widget.attrs['autofocus'] = True


    class Meta:
        model = notifIncidentesUsuarios
        fields = ['usuario_id']

        widgets = {
            'usuario_id': Select(attrs={
                'class': 'form-select form-control select2',
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                data['error'] = str(e)
        else:
            data['error'] = form.errors
        return data