from django import forms
from oPOSum.apps.layway.models import *
from django.utils.translation import ugettext as _

class LayawayForm(forms.ModelForm):
    class Meta:
        model = Layaway

class LayawayHistoryForm(forms.ModelForm):
    class Meta:
        model = LayawayHistory
