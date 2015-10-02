from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from oPOSum.apps.client.models import Client
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from decimal import Decimal

class LayawayManager(models.Manager):
    def can_add_more(self, client):
        ret = True
        ls = super(LayawayManager, self).get_query_set().filter(client = client)
        cnt = 0
        for l in ls:
            if l.get_debt_amount() > Decimal(0.0):
                cnt += 1
                if l.get_debt_amount() > (l.amount_to_pay * Decimal(0.3)):
                    ret = False
        if cnt > 2:
            ret = False
        #return ret
        return True

    def get_total_debt_amount(self, client):
        ret = Decimal(0)
        ls = Layaway.objects.filter(client = client)
        total = Decimal(0)
        for l in ls:
            total += l.get_debt_amount()
        return total

    def get_layaways(self, branch, datestart, dateend):
        layaways = super(LayawayManager, self).get_query_set().filter(branch__slug = branch).filter(date_time__range=(datestart, dateend)).order_by('date_time')

class Layaway(models.Model):
    ONE_MONTH = 30
    TWO_MONTHS = 60
    THREE_MONTHS = 90
    TYPES = (
        (ONE_MONTH, 'one_month'),
        (TWO_MONTHS, 'two_month'),
        (THREE_MONTHS, 'three_month'),
    )
    branch = models.ForeignKey(Branch)
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(_("Date and Time"), blank=True, null=False)
    amount_to_pay = models.DecimalField(_("Amount to Pay"), max_digits=10, decimal_places=2, default=Decimal(0.0))
    folio_number = models.PositiveIntegerField(_("Folio Number"), blank=True, null=True, default=0)
    type = models.IntegerField(_("Type"), choices=TYPES, default=ONE_MONTH)
    is_active = models.BooleanField(_("Is Active"), default = True)
    objects = LayawayManager()

    def get_debt_amount(self):
        lhs = LayawayHistory.objects.filter(layaway = self)
        ta = self.amount_to_pay
        pa = Decimal(0)
        for lh in lhs:
            pa += lh.amount
        return ta - pa

    def get_date_end(self):
        ets = self.date_time + timedelta(days=self.type)
        tz = timezone('America/Monterrey')
        return tz.normalize(ets.astimezone(tz))

    def update_amount_to_pay(self):
        ps = self.layawayproduct_set.all()
        total = Decimal(0.0)
        for p in ps:
            if p.price == Decimal(0.0):
                total += p.prod.get_retail_price() * Decimal(p.qty)
            else:
                total += p.price * Decimal(p.qty)
        self.amount_to_pay = total
        self.save()

    def get_last_payment(self):
        lh = LayawayHistory.objects.filter(layaway = self).order_by('date_time').last()
        return lh

    def as_json(self):
        tz = timezone('America/Monterrey')
        dt = tz.normalize(self.date_time.astimezone(tz))        
        return dict(
            id = self.id,
            branch = self.branch.slug,
            client = self.client.as_json(),
            products = [{'product': p.prod.as_json(),
                         'qty': p.qty, 'price': str(p.price)} for p in self.layawayproduct_set.all()],
            user = self.user.username,
            date_time = dt.strftime('%d/%m/%y %H:%M:%S'),
            amount_to_pay = "${0:.2f}=".format(self.amount_to_pay),
            total_debt_amount = "${0:.2f}=".format(self.get_debt_amount()),
            date_end = self.get_date_end().strftime('%d/%m/%y %H:%M:%S'),
            type = self.type
            )

    def save(self, *args, **kwargs):
        if not self.pk:
            dt = datetime.utcnow()
            self.date_time = pytz.utc.localize(dt)
        super(Layaway, self).save(*args, **kwargs)

class LayawayProduct(models.Model):
    prod = models.ForeignKey('products.Product')
    qty = models.PositiveIntegerField(_("Quantity"), default = 0)
    layaway = models.ForeignKey(Layaway)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, default=(Decimal(0.0)))

class LayawayHistoryManager(models.Manager):
    def get_payments_json(self, branch, datestart, dateend):
        payments = super(LayawayHistoryManager, self).get_query_set().filter(branch__slug = branch).filter(date_time__range=(datestart, dateend)).order_by('date_time')
        ret = [{'payment': p.as_json(), 
                'layaway': p.layaway.as_json()}
                for p in payments]
        return ret

class LayawayHistory(models.Model):
    branch = models.ForeignKey(Branch)
    user = models.ForeignKey(User)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(_("Date and Time"), auto_now=True)
    folio_number = models.PositiveIntegerField(_("Folio Number"), blank=True, null=True, default=0)
    payment_type = models.CharField(_("Payment Type"), max_length=255, default="Cash")
    layaway = models.ForeignKey(Layaway)
    objects = LayawayHistoryManager()

    def as_json(self):
        tz = timezone('America/Monterrey')
        dt = tz.normalize(self.date_time.astimezone(tz))        
        return dict(
            id = self.id,
            branch = self.branch.slug,
            user = self.user.username,
            amount = "${0:.2f}=".format(self.amount),
            date_time = dt.strftime('%d/%m/%Y %H:%M:%S'),
            payment_type = self.payment_type
        )
