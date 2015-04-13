from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from oPOSum.apps.inventory.models import Client
from datetime import datetime

class Layaway(models.Model):
    branch = models.ForeignKey(Branch)
    client = models.ForeignKey(Client)
    product = models.ManyToManyField(Product)
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)
    amount_to_pay = models.DecimalField(_("Amount to Pay"), max_digits=10, decimal_places=2)
    folio_number = models.PositiveIntegerField(_("Folio Number"))

class LayawayHistory(models.Model):
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)
    folio_number = models.PositiveIntegerField(_("Folio Number"))
    layaway = models.ForeignKey(Layaway)



# Create your models here.
