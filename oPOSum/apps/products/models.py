from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.inventory.models import ExistenceHistory, ExistenceHistoryDetail
from oPOSum.apps.pos.models import Sale, SaleDetails
from decimal import *
import logging
import json
import pytz
logger = logging.getLogger(__name__)

# Create your models here.
class ProviderDetail(models.Model):
    name = models.CharField(_("Name"), max_length=255, null=False, blank=False, default="detail name")
    description = models.CharField(_("Description"), max_length=255, null=False, blank=False, default="detail description")

class Provider(models.Model):
    sku = models.CharField(_("Codigo"), max_length = 3, blank = False, null = False, unique = True)
    name = models.CharField(_("Nombre"), max_length = 255, blank = False, null = False, default = "nombre")
    address = models.CharField(_("Direccion"), max_length = 255, blank = True, null = True)
    telephone1 = models.CharField(_("Telefono 1"), max_length = 255, blank = True, null = True)
    telephone2 = models.CharField(_("Telefono 2"), max_length = 255, blank = True, null = True)
    type = models.CharField(_("Tipo"), max_length=255)
    details = models.ManyToManyField(ProviderDetail)

    def __unicode__(self):
        return u'%s : %s' % (self.sku, self.name)

class ProductCategory(models.Model):
    name = models.CharField(_("Nombre"), max_length = 255)
    slug = models.SlugField(_("Codigo"), blank = False, unique = False)
    type = models.SlugField(_("Tipo"), blank = False, unique = False, 
        choices = (
            ('bodega', 'Bodega'),
            ('area', 'Area'),
            ('linea', 'Linea'),
            ('marca', 'Marca'),
            ('toons', 'Toons'),
        )
    )
    parent = models.ForeignKey('self', blank = True, null = True, related_name='child')
    description = models.TextField(_("Descripcion"), max_length = 255, blank=True)

    def __unicode__(self):
        return "%s : %s - %s" % (self.slug, self.name, self.type)

class ProductLine(models.Model):
    name = models.SlugField(_("Slug"), blank = True, unique=False)
    price = models.DecimalField(_("Price"), blank = False, max_digits=10, decimal_places=2)
    type = models.CharField(_("Type"), blank = False, unique=False, max_length = 5,
        choices = (
            ('10k', '10K'),
            ('14k', '14K'),
            ('plata', 'Plata'),
        )
    )

    def __unicode__(self):
        return "%s (%s) : %d" % (self.name, self.type, self.price)

class ProductDetail(models.Model):
    name = models.CharField(_("Name"), max_length=255, null=False, blank=False, default="detail name")
    description = models.CharField(_("Description"), max_length=255, null=False, blank=False, default="detail description")

class Product(models.Model):
    slug = models.CharField(_("Codigo"), max_length = 255, blank=True, unique=True)
    name = models.CharField(_("Nombre"), max_length = 255, blank=True, unique=False, null=True)
    provider = models.ForeignKey(Provider)
    category = models.ManyToManyField(ProductCategory, blank = True)
    line = models.ForeignKey(ProductLine, blank = True, null=True)
    regular_price = models.DecimalField(_("Precio"), blank = True, null = True, max_digits=10, decimal_places = 2, default=Decimal('0.00'))
    equivalency = models.DecimalField(_("Equivalencia"), blank = False, max_digits = 10, decimal_places = 2, default=Decimal('1.00'))
    description = models.TextField(_("Descripcion"), blank = True, max_length = 512)
    details = models.ManyToManyField(ProductDetail, blank = True)

    def __unicode__(self):
        return "%s : %s" % (self.slug, self.name)

    def as_json(self):
        logger.debug("Product's categories {0}".format(self.category.all()))
        ret = dict(
            name = self.name,
            slug = self.slug,
            provider = self.provider.name,
            categories = [dict(name = c.name, slug = c.slug, type = c.type) for c in self.category.all()],

            regular_price = str(self.regular_price),
            retail_price = str(self.get_retail_price()),
            equivalency = str(self.equivalency),
            description = self.description
        )
        if(self.line):
            ret['line'] = self.line.name
        return ret

    def get_retail_price(self):
        retail_price = Decimal(0.0)
        if self.regular_price == Decimal('0.00') and self.line is not None:
            retail_price = self.equivalency * self.line.price
        else:
            retail_price = self.regular_price
        return retail_price

    def get_transactions(self):
        logger.debug("Product's transactions {0}".format(self.name));
        ehs_positive = ExistenceHistoryDetail.objects.filter(product = self, existence__action='altas').order_by('existence__branch__name').order_by('existence__date_time')
        ehs_negative = ExistenceHistoryDetail.objects.filter(product = self, existence__action='bajas').order_by('existence__branch__name').order_by('existence__date_time')
        ehs_sales = SaleDetails.objects.filter(product = self).order_by('sale__branch__name').order_by('sale__date_time')
        r_positive = reduce(lambda x, y: x + y.quantity, ehs_positive, 0)
        r_negative = reduce(lambda x, y: x + y.quantity, ehs_negative, 0)
        r_sales = reduce(lambda x, y: x + y.quantity, ehs_sales, 0)
        total = r_positive - r_negative - r_sales;
        tz = pytz.timezone('America/Monterrey')
        entries = [dict(
                    quantity = o.quantity,
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in ehs_positive]
        exits = [dict(
                    quantity = str(o.quantity),
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in ehs_negative]
        sales = [dict(
                    branch = o.sale.branch.name,
                    date_time = o.sale.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    quantity = str(o.quantity),
                    folio_number = o.sale.folio_number
                    ) for o in ehs_sales]
        seen = set()
        branches = [o.existence.branch.name for o in ehs_positive if o.existence.branch.name not in seen and not seen.add(o.existence.branch.name) ]
        branches_transactions = {}
        for b in branches:
            qe = reduce(lambda x, y: x + y.quantity if y.existence.branch.name == b else x, ehs_positive, 0)
            qn = reduce(lambda x, y: x + y.quantity if y.existence.branch.name == b else x, ehs_negative, 0)
            qs = reduce(lambda x, y: x + y.quantity if y.sale.branch.name == b else x, ehs_sales, 0)
            branches_transactions[b] = dict(entries = qe, exits = qn, sales = qs)
        logger.debug("branches: {0}".format(branches_transactions))
        return dict(entries = entries, exits = exits, sales = sales, total=total, branches=branches, transactions_totals = branches_transactions)
        #return HttpResponse("{\"response\": \"ok\", \"entries\":" + json.dumps(entries) + ", \"exits\":" + json.dumps(exits) + ", \"sales\":" + json.dumps(sales) + "}", mimetypes="application/json");

