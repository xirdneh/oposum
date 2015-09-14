from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.inventory.models import ExistenceHistory, ExistenceHistoryDetail
from oPOSum.apps.pos.models import Sale, SaleDetails
from oPOSum.libs import utils as pos_utils
from decimal import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    def get_branch_transactions_count(self, branch):
        inves = self.inventoryentry_set.filter(inv__branch = branch, inv__enabled = False).order_by('-date_time')
        utc = pytz.timezone('UTC')
        if(len(inves) > 0):
            pinv = inves[0]
            dt = pinv.inv.date_time
        else:
            pinv = None
            dtu = datetime.utcnow()
            dt = dtu - relativedelta(years = 100)
        dt = dt.replace(tzinfo = utc)
        ehds_positive = self.existencehistorydetail_set.filter(existence__branch = branch, existence__date_time__gte = dt, existence__action = 'altas')
        ehds_negative = self.existencehistorydetail_set.filter(existence__branch = branch, existence__date_time__gte = dt, existence__action = 'bajas')
        sales = self.saledetails_set.filter(sale__branch = branch, sale__date_time__gte = dt)
        if pinv is not None:
            r_inv = pinv.quantity
        else:
            r_inv = 0
        r_positive = reduce(lambda x, y: x + y.quantity, ehds_positive, 0)
        r_negative = reduce(lambda x, y: x + y.quantity, ehds_negative, 0)
        r_sales = reduce(lambda x, y: x + y.quantity, sales, 0)
        return r_inv + r_positive - r_negative - r_sales

    def get_transactions(self):
        ret = {}
        inves = self.inventoryentry_set.filter(inv__enabled = False).order_by('inv').distinct('inv')
        inves = sorted(inves, key=lambda o: o.inv.date_time)
        invs = {}
        for i in inves:
            invs[i.inv.branch.name] = i.inv
        inves = []
        for key, val in invs.items():
            inves += self.inventoryentry_set.filter(inv = val)
        logger.debug("Inves: {0}".format(inves))
        ehs_positive = ExistenceHistoryDetail.objects.filter(product = self, existence__action='altas').order_by('existence__branch__name', 'existence__date_time')
        ehs_negative = ExistenceHistoryDetail.objects.filter(product = self, existence__action='bajas').order_by('existence__branch__name','existence__date_time')
        ehs_sales = SaleDetails.objects.filter(product = self).order_by('sale__branch__name', 'sale__date_time')
        r_positive = reduce(lambda x, y: x + y.quantity, ehs_positive, 0)
        r_einv = reduce(lambda x, y: x + y.quantity, inves, 0)
        r_negative = reduce(lambda x, y: x + y.quantity, ehs_negative, 0)
        r_sales = reduce(lambda x, y: x + y.quantity, ehs_sales, 0)
        total = r_positive + r_einv - r_negative - r_sales;
        tz = pytz.timezone('America/Monterrey')
        totales = {}
        entries = [dict(
                    quantity = o.quantity,
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in ehs_positive]
        for e in entries:
            if not e['branch'] in totales:
                totales[e['branch']] = dict(entries= 0, exits= 0, sales= 0, layaways= 0, inven = 0)
                totales[e['branch']]['entries'] = e['quantity']
            elif not 'entries' in totales[e['branch']]:
                totales[e['branch']]['entries'] = e['quantity']
            else:
                totales[e['branch']]['entries'] += e['quantity']

        inv_entries = [dict(
                    quantity = o.quantity,
                    id = o.inv.id,
                    branch = o.inv.branch.name,
                    date_time = o.inv.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
                    ) for o in inves]
        for e in inv_entries:
            if not e['branch'] in totales:
                totales[e['branch']] = dict(entries= 0, exits= 0, sales= 0, layaways= 0, inven=0)
                totales[e['branch']]['inven'] = e['quantity']
            elif not 'inven' in totales[e['branch']]:
                totales[e['branch']]['inven'] = e['quantity']
            else:
                totales[e['branch']]['inven'] += e['quantity']

        exits = [dict(
                    quantity = o.quantity,
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in ehs_negative]

        for e in exits:
            if not e['branch'] in totales:
                totales[e['branch']] = dict(entries= 0, exits= 0, sales= 0, layaways= 0, inven=0)
                totales[e['branch']]['exits'] = e['quantity']
            elif not 'exits' in totales[e['branch']]:
                totales[e['branch']]['exits'] = e['quantity']
            else:
                totales[e['branch']]['exits'] += e['quantity']

        sales = [dict(
                    branch = o.sale.branch.name,
                    date_time = o.sale.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    quantity = o.quantity,
                    folio_number = o.sale.folio_number
                    ) for o in ehs_sales if o.sale is not None ]

        for e in sales:
            if not e['branch'] in totales:
                totales[e['branch']] = dict(entries= 0, exits= 0, sales= 0, layaways= 0, inven=0)
                totales[e['branch']]['sales'] = e['quantity']
            elif not 'sales' in totales[e['branch']]:
                totales[e['branch']]['sales'] = e['quantity']
            else:
                totales[e['branch']]['sales'] += e['quantity']

        ret['entries'] = entries
        ret['exits'] = exits
        ret['sales'] = sales
        ret['inven'] = inv_entries
        ret['totals'] = dict(
                total = total,
                entries = r_positive,
                inven = r_einv,
                exits = r_negative,
                sales = r_sales)
        apps = pos_utils.get_installed_oposum_apps()
        if 'layaway' in apps:
            from oPOSum.apps.layaway.models import LayawayProduct
            lay_prods = LayawayProduct.objects.filter(prod = self).order_by('layaway__branch__name', 'layaway__date_time')
            layaways = [dict(
                    quantity = o.qty,
                    id = o.layaway.id,
                    branch = o.layaway.branch.name,
                    date_time = o.layaway.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
                    ) for o in lay_prods]

            for e in layaways:
                if not e['branch'] in totales:
                    totales[e['branch']] = dict(entries= 0, exits= 0, sales= 0, layaways= 0, inven=0)
                    totales[e['branch']]['layaways'] = e['quantity']
                elif not 'layaways' in totales[e['branch']]:
                    totales[e['branch']]['layaways'] = e['quantity']
                else:
                    totales[e['branch']]['layaways'] += e['quantity']

            ret['layaways'] = layaways
            ret['totals']['layaways'] = reduce(lambda x, y: x + y.qty, lay_prods, 0)
        if 'workshop' in apps:
            from oPOSum.apps.workshop.models import WorkshopProduct
            ws_prods = WorkshopProduct.objects.filter(product = self).order_by('ticket__branch__name', 'ticket__date_time')
            workshops = [dict(
                    quantity = o.qty,
                    id = o.ticket.id,
                    branch = o.ticket.branch.name,
                    date_time = o.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
                    ) for o in ws_prods]

            for e in workshops:
                if not e['branch'] in totales:
                    totales[e['branch']] = dict(entries= 0, exits= 0, sales= 0, layaways= 0, inven=0)
                    totales[e['branch']]['workshops'] = e['quantity']
                elif not 'workshops' in totales[e['branch']]:
                    totales[e['branch']]['workshops'] = e['quantity']
                else:
                    totales[e['branch']]['workshops'] += e['quantity']

            ret['workshops'] = workshops
            ret['totals']['workshops'] = reduce(lambda x, y: x + y.qty, ws_prods, 0)
        logger.debug("totals: {0}".format(totales))
        for b, t in totales.items():
            totales[b]['actual'] = t['inven'] + t['entries'] - t['exits'] - t['sales'] - t['layaways']
        ret['totals']['tot_branches'] = totales
        return ret
