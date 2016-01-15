from django.db import models
from django.utils.translation import ugettext as _
#from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from decimal import Decimal
import logging, traceback
import pytz
import json
from collections import OrderedDict
logger = logging.getLogger(__name__)

# Create your models here.
class SaleManager(models.Manager):
    def get_sales(self, branch, datestart, dateend):
        sales = super(SaleManager, self).get_query_set().filter(branch__slug = branch).filter(date_time__range=(start_date, end_date)).order_by('date_time')
        return sales

    def get_sales_structure(self, branch, datestart, dateend):
        sales = super(SaleManager, self).get_query_set().filter(branch__slug = branch).filter(date_time__range=(datestart, dateend)).order_by('date_time')
        tz = pytz.timezone('America/Monterrey')
        ret = {}
        date = None
        local_date = None
        total = Decimal(0)
        totales = {}
        for s in sales:
            date = s.date_time.date()
            local_date = s.date_time.astimezone(tz)
            date_s = local_date.strftime("%Y-%m-%d")
            if date_s not in ret:
                ret[date_s] = {}
                ret[date_s]['all_sales'] = []
            #logger.debug("dt: {0}".format(date_s))
            ret[date_s]["all_sales"].append({})
            ret[date_s]["all_sales"][-1]["sale"] = s
            ret[date_s]["all_sales"][-1]["sales"] = []
            #logger.debug("ret[date_s] {0}".format(ret[date_s]))
            #logger.debug("sale: {0}".format(s))
            total += Decimal(s.total_amount)
            sds = SaleDetails.objects.filter(sale = s)
            key = ''
            for sd in sds:
                ret[date_s]["all_sales"][-1]["sales"].append(sd)
                bodega = sd.product.get_category('bodega')
                if not bodega:
                    bodega = ''
                else:
                    bodega = bodega.slug
               
                area = sd.product.get_category('area')
                if not area:
                    area = ''
                else:
                    area = area.slug
                
                linea = sd.product.get_category('linea')
                if not linea:
                    linea = ''
                else:
                    linea = linea.slug
                code = sd.product.name.split('-')
                if len(code) >= 2:
                    letter = code[1][:1].lower()
                else:
                    letter = ''
                if sd.product.slug[:2] == '17':
                    key = 'Relojes'
                elif bodega == '6' or letter == 'c':
                    key = 'Chapa'
                elif area == 'A' or letter == 'a':
                    key = 'Acero'
                elif letter == 'b':
                    key = 'Bisuteria'
                elif bodega in ['1', '2', '3', '5', '7', '8'] or letter in ['1', '2']:
                    key = 'Oro'
                elif bodega == '16' or letter == 'p':
                    key = 'Plata'
                else:
                    if '-DESC' not in sd.product.name:
                        key = 'Taller'

                if date_s not in totales:
                    totales[date_s] = {}
                if key not in totales[date_s]:
                    totales[date_s][key] = {}
                    totales[date_s][key]['total'] = Decimal(0)
                    totales[date_s][key]['sd'] = []
                if key != '':
                    totales[date_s][key]['sd'].append({'sd': sd, 'sale':s.as_json()})
                    totales[date_s][key]['total'] += Decimal(sd.over_price) * Decimal(sd.quantity)

            ret[date_s]["total"] = str(total)
        #ret = [sale.as_json() for sale in sales]
        return {'sales': OrderedDict(sorted(ret.items()), key=lambda t:t[0]), 
                'totales': OrderedDict(sorted(totales.items()), key=lambda t:t[0]), 
                'folio_start': sales.first().folio_number, 
                'folio_end': sales.last().folio_number}

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
