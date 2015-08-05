from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from oPOSum.apps.client.models import Client
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from decimal import Decimal

class WorkshopTicketManager(models.Manager):

    def get_total_debt_amount(self, client):
        ret = Decimal(0.0)
        tickets = super(self, WorkshopTicketManager).get_query_set().filter(client = client)
        for t in tickets:
            payments = tickets.workshoppayment_set.all()

class WorkshopTicket(models.Model):
    branch = models.ForeignKey(Branch)
    client = models.ForeignKey(Client, null=True)
    user = models.User(user)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add = True)
    date_time_end = models.DateTimeField(_("Date and Time of Delivery"), blank = True, null = False)
    folio_number = models.PositiveIntegerField(_("Folio Number"), blank = True, null = True, default = 0)
    workshop = models.ForeignKey(Branch)
    total_cost = models.DecimalField(_("Total Cost"), max_digits=10, decimal_places=2, default = Decimal(0.0))
    time_to_complete = models.PositiveIntegerField(_("Time to Complete"), default = 5)
    current_location = models.ForeignKey(Branch)
    is_active = models.BooleanField(_("Is Active"), default=True)
    objects = WorkshopTicketManager()

    def update_total_cost(self):
        services = self.workshopservices_set.all()
        products = self.workshopproduct_set.all()
        total = Decimal(0.0)
        for p in products:
            total += p.prod.get_retail_price() * Decimal(p.qty)
        for s in services:
            total += s.amount
        self.tota_cost = total
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            dt = datetime.utcnow()
            self.date_time_end = pytz.utc.localize(dt)
        super(WorkshopTicket, self).save(*args, **kwargs)

class WorkshopPayment(models.Model):
    branch = models.ForeignKey(Branch)
    user = models.ForeignKey(User)
    ticket = models.ForeignKey(WorkshopTicket)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add = True)
    amount = models.DecimalField(_("Amount to Pay"), max_digits=10, decimal_places=2, default = Decimal(0.0))
    payment_tye = models.CharField(_("Payment type"), max_length=255, default="Cash")

class WorkshopStatus(models.Model):
    branch = models.ForeignKey(Branch)
    user = models.ForeignKey(User)
    ticket = models.ForeignKey(WorkshopTicket)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add = True)
    description = models.TextField(_("Description"), null = False, blank = False, default = "Description")
    is_current = models.BooleanField(_("Is Current"), default = False)

class WorkshopServices(models.Model):
    branch = models.ForeignKey(Branch)
    user = models.ForeignKey(User)
    ticket = models.ForeignKey(WorkshopTicket)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add = True)
    description = models.TextField(_("Description"), null = False, blank = False, default = "Description")
    amount = models.DecimalField(_("Amount to Pay"), max_digits=10, decimal_places=2, default = Decimal(0.0))

class WorkshopProduct(models.Model):
    branch = models.ForeignKey(Branch)
    user = models.ForeignKey(User)
    ticket = models.ForeignKey(WorkshopTicket)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add = True)
    product = models.ForeignKey(Product)
    qty = models.PositiveIntegerField(_("Quantity"), blank = False, null = False, default = 0)
