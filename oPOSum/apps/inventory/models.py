from django.db import models
from django.utils.translation import ugettext as _
#from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Existence(models.Model):
    product = models.ForeignKey('products.Product')
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    branch = models.ForeignKey(Branch)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)

class ExistenceHistory(models.Model):
    folio_number = models.PositiveIntegerField(_("Folio Number"), blank=True, null=True)
    user = models.ForeignKey(User)
    branch = models.ForeignKey(Branch)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)
    action = models.CharField(_("Action"), max_length=255, blank=False, null=False,
        choices = (
            (u'altas', u'Altas'),
            (u'bajas', u'Bajas'),
            (u'baja_tras', u'baja_tras'),
            (u'alta_tras', u'alta_tras'),
        ),
    )
    printed = models.BooleanField(_("Enabled"), default=False)
    extra = models.CharField(_("Extra"), max_length=1024, blank=True, null=True)
    details = models.TextField(_("Details"), blank=True, null=True)

    def __unicode__(self):
        return "{0}: {1} - {2}".format(self.id, self.branch.slug, self.date_time)

    def as_json(self):
        return dict(
            id = self.id,
            user = self.user.username,
            branch = self.branch.slug,
            branch_name = self.branch.name,
            date_time = self.date_time.strftime('%d-%b-%Y %H:%M:%S'),
            action = self.action,
            extra = self.extra            
        )

class ExistenceHistoryDetail(models.Model):
    product = models.ForeignKey('products.Product')
    quantity = models.PositiveIntegerField(_("Quantity"), default = 1)
    existence = models.ForeignKey(ExistenceHistory, blank=True, null=True)

    def __unicode__(self):
        return "{0}: {1} - {2}: {3}".format(self.id, self.product.slug, self.quantity, self.existence.id)

    def as_json(self):
        return dict(
            product = self.product.name,
            description = self.product.description,
            quantity = self.quantity
        )        

class InventoryFolio(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    value = models.PositiveIntegerField(_("Value"))

class Inventory(models.Model):
    branch = models.ForeignKey(Branch, default = 0)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add = True)
    enabled = models.BooleanField(_("Enabled"), default=False)
    comments = models.TextField(_("Comments"), max_length=1024, blank=True)
    adjusting = models.BooleanField(_("Adjusting"), default= False)

    def __unicode__(self):
        return "{0} - {1}".format(self.branch, self.date_time.strftime('%Y-%m-%d'))

class InventoryEntry(models.Model):
    inv = models.ForeignKey(Inventory, blank=True)
    product = models.ForeignKey('products.Product')
    quantity = models.PositiveIntegerField(_("Quantity"), default = 1)
    date_time = models.DateTimeField(_("Date and Time"), auto_now = True, default = datetime.now)
    user = models.ForeignKey(User)

    def as_json(self):
        return dict(
            id = self.id,
            slug = self.product.slug,
            desc = self.product.description,
            qty = self.quantity
        )

    def get_adjustment_count(self):
        return reduce(lambda x, y: x + y.quantity, self.inventoryadjustment_set.all(), 0)

class InventoryAdjustment(models.Model):
    inventory_entry = models.ForeignKey(InventoryEntry)
    quantity = models.IntegerField(_("Quantity"), default = 0, blank = False, null = False)
    message = models.TextField(_("Message"), default = "", blank = False, null = False)

    def as_json(self):
        return dict(
            id = self.id,
            inventory_entry = self.inventory_entry.as_json(),
            quantity = self.quantity,
            message = self.message
        )

class ProductTransfer(models.Model):
    branch_from = models.ForeignKey('branches.Branch', related_name='from')
    branch_to = models.ForeignKey('branches.Branch', related_name='to')
    status = models.TextField(_("Status"), max_length = 255, blank=False, null=False)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add=True)
    user = models.ForeignKey(User)

class ProductTransferDetail(models.Model):
    product = models.ForeignKey('products.Product')
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    product_transfer = models.ForeignKey(ProductTransfer)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add=True)

class ProductTransferHistory(models.Model):
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)
    status_previous = models.TextField(_("Status Previous"), max_length = 255, blank=False, null=False)
    status_changed = models.TextField(_("Status Changed"), max_length = 255, blank=False, null=False)
    product_transfer = models.ForeignKey(ProductTransfer)
    user = models.ForeignKey(User)
