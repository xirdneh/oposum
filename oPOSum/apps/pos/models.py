from django.db import models
from django.utils.translation import ugettext as _
#from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from decimal import Decimal
import logging, traceback
import pytz
logger = logging.getLogger(__name__)

# Create your models here.
class SaleManager(models.Manager):
    def get_sales(self, branch, datestart, dateend):
        sales = super(SaleManager, self).get_query_set().filter(branch__slug = branch).filter(date_time__range=(start_date, end_date)).order_by('date_time')
        return sales

    def get_sales_structure(self, branch, datestart, dateend):
        logger.info('datestart: {0}'.format(datestart))
        logger.info('dateend: {0}'.format(dateend))
        sales = super(SaleManager, self).get_query_set().filter(branch__slug = branch).filter(date_time__range=(datestart, dateend)).order_by('date_time')
        tz = pytz.timezone('America/Monterrey')
        ret = {}
        date = None
        local_date = None
        total = Decimal(0)
        for s in sales:
            local_date = s.date_time.date().astimezone(tz)
            if date != local_date:
                total = Decimal(0)
                date = local_date
                date_s = date.strftime("%Y-%m-%d")
                ret[date_s] = {}
                ret[date_s]["all_sales"] = []
            else:
                date_s = date.strftime("%Y-%m-%d")
            #logger.debug("dt: {0}".format(date_s))
            ret[date_s]["all_sales"].append({})
            ret[date_s]["all_sales"][-1]["sale"] = s
            ret[date_s]["all_sales"][-1]["sales"] = []
            #logger.debug("ret[date_s] {0}".format(ret[date_s]))
            #logger.debug("sale: {0}".format(s))
            total += Decimal(s.total_amount)
            sds = SaleDetails.objects.filter(sale = s)
            for sd in sds:
                logging.debug("sale details: {0}".format(sd))
                ret[date_s]["all_sales"][-1]["sales"].append(sd)
            ret[date_s]["total"] = str(total)
        #ret = [sale.as_json() for sale in sales]
        logger.debug("ret {0}".format(ret))
        return ret

    def get_sales_json(self, branch, datestart, dateend):
        sales = super(SaleManager, self).get_query_set().filter(branch__slug = branch).filter(date_time__range=(datestart, dateend)).order_by('date_time')
        logger.debug("ret {0}".format(sales))
        ret = [sale.as_json() for sale in sales]
        return ret

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
    is_active = models.BooleanField(_("Is Active"), default = True)
    objects = SaleManager()

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
            ticket_post = self.branch.ticket_post.encode('unicode_escape'),
            sale_details = [sd.as_json() for sd in self.saledetails_set.all()]
            )

class SaleDetails(models.Model):
    product = models.ForeignKey('products.Product')
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    over_price = models.DecimalField(_("Overwritten Price"), max_digits = 10, decimal_places=2, blank=True, null=True)
    sale = models.ForeignKey(Sale, blank=True, null=True)

    def __unicode__(self):
        return "%s: %f" % (self.sale, self.over_price)

    def as_json(self):
        return dict(
            product = self.product.as_json(),
            quantity = str(self.quantity),
            over_price = str(self.over_price)
        )

class POSFolio(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    value = models.PositiveIntegerField(_("Value"))
    branch = models.ForeignKey(Branch, blank = True, null = True)
