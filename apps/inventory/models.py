from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User

# Create your models here.
class Existence(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    branch = models.ForeignKey(Branch)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)

class ExistenceHistory(models.Model):
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)
    action = models.CharField(_("Action"), max_length=255, blank=False, null=False,
        choices = (
            (u'altas', u'Altas'),
            (u'bajas', u'Bajas'),
        ),
    )
    extra = models.CharField(_("Extra"), max_length=1024, blank=True, null=True)

class ExistenceHistoryDetail(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(_("Quantity"), default = 1)
    existence = models.ForeignKey(ExistenceHistory, blank=True, null=True)

class Client(models.Model):
    first_name = models.CharField(_("First Name"), max_length=100, blank=True)
    last_name = models.CharField(_("Last Name"), max_length = 512, blank=True)
    phonenumber = models.CharField(_("Phone Number"), max_length=512, blank=True)
    address = models.TextField(_("Address"), max_length=1024, blank=True)
    id_number = models.TextField(_("Identification Number"), max_length=255, blank=True)

class InventoryFolio(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    value = models.PositiveIntegerField(_("Value"))
