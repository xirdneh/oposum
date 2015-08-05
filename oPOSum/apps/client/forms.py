# -*- coding: utf-8
from django import forms
from django.utils.translation import ugettext as _
from oPOSum.apps.client.models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phonenumber', 'email', 'id_type', 'id_number', 'address']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phonenumber': 'Número de Telefono',
            'address': 'Dirección', 
            'id_type': 'Tipo de identificación',
            'id_number': 'Número de identificación',
            'email': 'Correo Electrónico',
        }
