from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from oPOSum.apps.inventory.models import Client

# Create your models here.
class Sale(models.Model):
    #product = models.ManyToManyField(Product)
    #quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    branch = models.ForeignKey(Branch)
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)
    total_amount = models.DecimalField(_("Total Amount"), max_digits = 10, decimal_places=2)
    payment_method = models.CharField(_("Payment Method"), max_length=255, default="Cash")
    payment_amount = models.DecimalField(_("Payment Amount"), max_digits = 10, decimal_places=2)
    extra = models.CharField(_("Extra"), max_length=1024, blank=True, null=True)
    folio_number = models.PositiveIntegerField(_("Folio Number"))

    def __unicode__(self):
        return "%s: %s" % (self.branch, str(self.folio_number))

    def as_json(self):
        return dict(
            branch = self.branch.slug,
            user = self.user.username,
            date_time = self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            total_amount = str(self.total_amount),
            payment_method = self.payment_method,
            payment_amount = str(self.payment_amount),
            folio_number = self.folio_number,
            ticket_pre = self.branch.ticket_pre.encode('unicode_escape'),
            ticket_post = self.branch.ticket_post.encode('unicode_escape')
            )

class SaleDetails(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    over_price = models.DecimalField(_("Overwritten Price"), max_digits = 10, decimal_places=2, blank=True, null=True)
    sale = models.ForeignKey(Sale, blank=True, null=True)

    def __unicode__(self):
        return "%s: %f" % (self.sale, self.over_price)

class Layaway(models.Model):
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

class POSFolio(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    value = models.PositiveIntegerField(_("Value"))
    branch = models.ForeignKey(Branch, blank = True, null = True)
