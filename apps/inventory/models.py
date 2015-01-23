from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Existence(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    branch = models.ForeignKey(Branch)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)

class ExistenceHistory(models.Model):
    folio_number = models.PositiveIntegerField(_("Folio Number"))
    user = models.ForeignKey(User)
    branch = models.ForeignKey(Branch)
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

class Inventory(models.Model):
    branch = models.ForeignKey(Branch, default = 0)
    date_time = models.DateTimeField(_("Date and Time"), auto_now = True)
    enabled = models.BooleanField(_("Enabled"), default=False)
    comments = models.TextField(_("Comments"), max_length=1024, blank=True)

    def __unicode__(self):
        return "{0} - {1}".format(self.branch, self.date_time.strftime('%Y-%m-%d'))

class InventoryEntry(models.Model):
    inv = models.ForeignKey(Inventory, blank=True)
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(_("Quantity"), default = 1)
    date_time = models.DateTimeField(_("Date and Time"), auto_now = True, default = datetime.now)
    user = models.ForeignKey(User)

    def as_json(self):
        return dict(
            slug = self.product.slug,
            desc = self.product.description,
            qty = self.quantity
        )
