from django.db import models
from django.utils.translation import ugettext as _
from oPOSum.apps.inventory.models import ExistenceHistory, ExistenceHistoryDetail, ProductTransfer, ProductTransferDetail
from oPOSum.apps.pos.models import Sale, SaleDetails
from oPOSum.apps.branches.models import Branch
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
    def has_category(self, ctype, cslug):
        cats = self.category.all().filter(slug = cslug, type = ctype)
        return len(cats) > 0

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
        branches = Branch.objects.all()
        tz = pytz.timezone('America/Monterrey')
        ret = {}
        ret['layaways'] = []
        ret['exits'] = []
        ret['workshops'] = []
        ret['sales'] = []
        ret['totals'] = {}
        ret['totals']['tot_branches'] = {}
        ret['totals']['total'] = 0
        ret['inven'] = []
        ret['entries'] = []
        ret['entries_tras'] = []
        ret['exits_tras'] = []
        ret['tras_from'] = []
        ret['tras_to'] = []
        apps = pos_utils.get_installed_oposum_apps()
        for branch in branches:
            qty = 0
            logger.info('Branch: {0}'.format(branch.name))
            if branch.name not in ret['totals']['tot_branches']:
                ret['totals']['tot_branches'][branch.name] = {}
                ret['totals']['tot_branches'][branch.name]['slug'] = branch.slug
            inventory = self.inventoryentry_set.filter(inv__enabled = False, 
                                                       inv__branch = branch).order_by('date_time') 
            logger.info('Inventory: {0}'.format(len(inventory)))
            if len(inventory) > 0:
                inventory = inventory.last()
                if inventory.quantity > 0:
                    ret['inven'] += [dict(
                        quantity = inventory.quantity,
                        id = inventory.inv.id,
                        branch = inventory.inv.branch.name,
                        branch_slug = inventory.inv.branch.slug,
                        date_time = inventory.inv.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
                        )]
                    qty = inventory.quantity
                    if 'inven' not in ret['totals']['tot_branches'][branch.name]:
                        ret['totals']['tot_branches'][branch.name]['inven'] = 0
                    ret['totals']['tot_branches'][branch.name]['inven'] += qty
                    if 'inven' not in ret['totals']:
                        ret['totals']['inven'] = 0
                    ret['totals']['inven'] += qty
                else:
                    inventory = None
                    ret['totals']['tot_branches'][branch.name]['inven'] = 0
                    if 'inven' not in ret['totals']:
                        ret['totals']['inven'] = 0
                             
            else:
                inventory = None
                ret['totals']['tot_branches'][branch.name]['inven'] = 0
                if 'inven' not in ret['totals']:
                    ret['totals']['inven'] = 0
            qty = 0
            altas = ExistenceHistoryDetail.objects.filter(product = self, 
                                                          existence__action = 'altas', 
                                                          existence__branch = branch).order_by('existence__date_time')
            logger.info('Entries: {0}'.format(len(altas)))
            if inventory is not None:
                altas = altas.filter(existence__date_time__gte = inventory.date_time)
            logger.info('Entries date: {0}'.format(len(altas)))
            b_entries = [dict(
                    quantity = o.quantity,
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    branch_slug = o.existence.branch.slug,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in altas]
            ret['entries'] += b_entries
            qty = reduce(lambda x, y: x + y['quantity'], b_entries, 0)

            if 'entries' not in ret['totals']['tot_branches'][branch.name]:
                ret['totals']['tot_branches'][branch.name]['entries'] = 0
            ret['totals']['tot_branches'][branch.name]['entries'] += qty
            if 'entries' not in ret['totals']:
                ret['totals']['entries'] = 0
            ret['totals']['entries'] += qty
            qty = 0
            altas_tras = ExistenceHistoryDetail.objects.filter(product = self,
                                                               existence__action = 'alta_tras',
                                                               existence__branch = branch).order_by('existence__date_time')
            if inventory is not None:
                altas_tras = altas_tras.filter(existence__date_time__gte = inventory.date_time)
            b_entries_tras = [dict(
                    quantity = o.quantity,
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    branch_slug = o.existence.branch.slug,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in altas_tras]
            qty = reduce(lambda x, y: x + y['quantity'], b_entries_tras, 0)
            ret['entries_tras'] += b_entries_tras

            if 'entries_tras' not in ret['totals']['tot_branches'][branch.name]:
                ret['totals']['tot_branches'][branch.name]['entries_tras'] = 0
            ret['totals']['tot_branches'][branch.name]['entries_tras'] += qty
            if 'entries_tras' not in ret['totals']:
                ret['totals']['entries_tras'] = 0
            ret['totals']['entries_tras'] += qty
            qty = 0
            bajas = ExistenceHistoryDetail.objects.filter(product = self,
                                                          existence__action = 'bajas',
                                                          existence__branch = branch).order_by('existence__date_time')
            if inventory is not None:
                bajas = bajas.filter(existence__date_time__gte = inventory.date_time)
            b_exits = [dict(
                    quantity = o.quantity,
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    branch_slug = o.existence.branch.slug,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in bajas]
            qty = reduce(lambda x, y: x + y['quantity'], b_exits, 0)
            ret['exits'] += b_exits

            if 'exits' not in ret['totals']['tot_branches'][branch.name]:
                ret['totals']['tot_branches'][branch.name]['exits'] = 0
            ret['totals']['tot_branches'][branch.name]['exits'] += qty
            if 'exits' not in ret['totals']:
                ret['totals']['exits'] = 0
            ret['totals']['exits'] += qty

            qty = 0
            bajas_tras = ExistenceHistoryDetail.objects.filter(product = self,
                                                               existence__action = 'baja_tras',
                                                               existence__branch = branch).order_by('existence__date_time')
            if inventory is not None:
                bajas_tras = bajas_tras.filter(existence__date_time__gte = inventory.date_time)
            b_exits_tras = [dict(
                    quantity = o.quantity,
                    id = o.existence.id,
                    branch = o.existence.branch.name,
                    branch_slug = o.existence.branch.slug,
                    date_time = o.existence.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in bajas_tras]
            qty = reduce(lambda x, y: x + y['quantity'], b_exits_tras, 0)
            ret['exits_tras'] += b_exits_tras

            if 'exits_tras' not in ret['totals']['tot_branches'][branch.name]:
                ret['totals']['tot_branches'][branch.name]['exits_tras'] = 0
            ret['totals']['tot_branches'][branch.name]['exits_tras'] += qty
            if 'exits_tras' not in ret['totals']:
                ret['totals']['exits_tras'] = 0
            ret['totals']['exits_tras'] += qty

            qty = 0
            sales = SaleDetails.objects.filter(product = self, 
                                               sale__branch = branch, 
                                               sale__is_active = True).order_by('sale__date_time')
            if inventory is not None:
                sales = sales.filter(sale__date_time__gte = inventory.date_time)
            b_sales = [dict(
                    branch = o.sale.branch.name,
                    branch_slug = o.sale.branch.slug,
                    date_time = o.sale.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    quantity = o.quantity,
                    folio_number = o.sale.folio_number
                    ) for o in sales]
            qty = reduce(lambda x, y: x + y['quantity'], b_sales, 0)
            ret['sales'] += b_sales
            if 'sales' not in ret['totals']['tot_branches'][branch.name]:
                ret['totals']['tot_branches'][branch.name]['sales'] = 0
            ret['totals']['tot_branches'][branch.name]['sales'] += qty
            if 'sales' not in ret['totals']:
                ret['totals']['sales'] = 0
            ret['totals']['sales'] += qty

            qty = 0
            transfers_from = ProductTransferDetail.objects.filter(product = self, 
                                                                  product_transfer__branch_from = branch).order_by('product_transfer__date_time')
            if inventory is not None:
                transfers_from = transfers_from.filter(product_transfer__date_time__gte = inventory.date_time)
            b_tras_from = [dict(
                    quantity = o.quantity,
                    id = o.product_transfer.id,
                    branch_from = o.product_transfer.branch_from.name,
                    branch_from_slug = o.product_transfer.branch_from.slug,
                    branch_to = o.product_transfer.branch_to.name,
                    branch_to_slug = o.product_transfer.branch_to.slug,
                    date_time = o.product_transfer.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in transfers_from]
            qty = reduce(lambda x, y: x + y['quantity'], b_tras_from, 0)
            ret['tras_from'] += b_tras_from

            if 'tras_from' not in ret['totals']['tot_branches'][branch.name]:
                ret['totals']['tot_branches'][branch.name]['tras_from'] = 0
            ret['totals']['tot_branches'][branch.name]['tras_from'] += qty
            if 'tras_from' not in ret['totals']:
                ret['totals']['tras_from'] = 0
            ret['totals']['tras_from'] += qty

            qty = 0
            transfers_to = ProductTransferDetail.objects.filter(product = self, 
                                                                product_transfer__branch_to = branch).order_by('product_transfer__date_time')
            if inventory is not None:
                transfers_to = transfers_to.filter(product_transfer__date_time__gte = inventory.date_time)

            b_tras_to = [dict(
                    quantity = o.quantity,
                    id = o.product_transfer.id,
                    branch_from = o.product_transfer.branch_from.name,
                    branch_from_slug = o.product_transfer.branch_from.slug,
                    branch_to = o.product_transfer.branch_to.name,
                    branch_to_slug = o.product_transfer.branch_to.slug,
                    date_time = o.product_transfer.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                    ) for o in transfers_to] 
            qty = reduce(lambda x, y: x + y['quantity'], b_tras_to, 0)
            ret['tras_to'] += b_tras_to

            if 'tras_to' not in ret['totals']['tot_branches'][branch.name]:
                ret['totals']['tot_branches'][branch.name]['tras_to'] = 0
            ret['totals']['tot_branches'][branch.name]['tras_to'] += qty
            if 'tras_to' not in ret['totals']:
                ret['totals']['tras_to'] = 0
            ret['totals']['tras_to'] += qty

            if 'layaway' in apps:
                qty = 0
                from oPOSum.apps.layaway.models import LayawayProduct
                layaways = LayawayProduct.objects.filter(prod = self, 
                                                         layaway__is_active = True, 
                                                         layaway__branch = branch).order_by('layaway__date_time')
                if inventory is not None:
                    layaways = layaways.filter(layaway__date_time__gte = inventory.date_time)
                b_layaways = [dict(
                        quantity = o.qty,
                        id = o.layaway.id,
                        branch = o.layaway.branch.name,
                        branch_slug = o.layaway.branch.slug,
                        date_time = o.layaway.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
                        ) for o in layaways]
                qty = reduce(lambda x, y: x + y['quantity'], b_layaways, 0)
                ret['layaways'] += b_layaways

                if 'layaways' not in ret['totals']['tot_branches'][branch.name]:
                    ret['totals']['tot_branches'][branch.name]['layaways'] = 0
                ret['totals']['tot_branches'][branch.name]['layaways'] += qty
                if 'layaways' not in ret['totals']:
                    ret['totals']['layaways'] = 0
                ret['totals']['layaways'] += qty
            
            if 'workshop' in apps:
                qty = 0
                from oPOSum.apps.workshop.models import WorkshopProduct
                workshop_tickets = WorkshopProduct.objects.filter(product = self, 
                                                          ticket__is_active = True,
                                                          ticket__branch = branch).order_by('ticket__date_time')
                if inventory is not None:
                    inventory = workshop_tickets.filter(ticket__date_time__gte = inventory.date_time)

                b_workshops = [dict(
                    quantity = o.qty,
                    id = o.ticket.id,
                    branch = o.ticket.branch.name,
                    branch_slug = o.ticket.branch.slug,
                    date_time = o.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
                    ) for o in workshop_tickets]
                qty = reduce(lambda x, y: x + y['quantity'], b_workshops, 0)
                ret['workshops'] += b_workshops

                if 'workshops' not in ret['totals']['tot_branches'][branch.name]:
                    ret['totals']['tot_branches'][branch.name]['workshops'] = 0
                ret['totals']['tot_branches'][branch.name]['workshops'] += qty
                if 'workshops' not in ret['totals']:
                    ret['totals']['workshops'] = 0
                ret['totals']['workshops'] += qty
                
            b_actual = ret['totals']['tot_branches'][branch.name]['inven'] + ret['totals']['tot_branches'][branch.name]['entries'] - ret['totals']['tot_branches'][branch.name]['exits'] + ret['totals']['tot_branches'][branch.name]['entries_tras'] - ret['totals']['tot_branches'][branch.name]['exits_tras'] - ret['totals']['tot_branches'][branch.name]['sales'] - ret['totals']['tot_branches'][branch.name]['layaways']
            ret['totals']['tot_branches'][branch.name]['actual'] = b_actual
            ret['totals']['total'] += b_actual

            #logger.info('======================================================')
            #logger.info('object: {0}'.format(json.dumps(ret, indent=4)))
        return ret


'''
{
    "layaways": [
        {
            "date_time": "2015-12-05 19:10:12",
            "id": 870,
            "branch": "Grande Campestre",
            "quantity": 2
        }
    ],
    "exits": [],
    "workshops": [],
    "sales": [
        {
            "date_time": "2015-11-28 18:35:05",
            "folio_number": 437,
            "branch": "Grande Campestre",
            "quantity": 1
        },
        {
            "date_time": "2015-06-28 11:18:53",
            "folio_number": 2232,
            "branch": "Ocho HIdalgo",
            "quantity": 2
        },
        {
            "date_time": "2015-07-17 13:49:36",
            "folio_number": 4758,
            "branch": "Ocho HIdalgo",
            "quantity": 2
        }
    ],
    "totals": {
        "layaways": 2,
        "exits": 0,
        "tot_branches": {
            "Once Hidalgo": {
                "layaways": 0,
                "actual": 2,
                "exits": 0,
                "sales": 0,
                "inven": 2,
                "entries": 0
            },
            "Grande Campestre": {
                "layaways": 2,
                "actual": 2,
                "exits": 0,
                "sales": 1,
                "inven": 3,
                "entries": 2
            },
            "HEB Lincoln": {
                "layaways": 0,
                "actual": 2,
                "exits": 0,
                "sales": 0,
                "inven": 2,
                "entries": 0
            },
            "Soriana Palmas": {
                "layaways": 0,
                "actual": 2,
                "exits": 0,
                "sales": 0,
                "inven": 2,
                "entries": 0
            },
            "Ocho HIdalgo": {
                "layaways": 0,
                "actual": 2,
                "exits": 0,
                "sales": 4,
                "inven": 2,
                "entries": 4
            }
        },
        "workshops": 0,
        "sales": 5,
        "inven": 11,
        "entries": 6,
        "total": 12
    },
    "inven": [
        {
            "date_time": "2015-09-14 09:30:21",
            "id": 12,
            "branch": "Once Hidalgo",
            "quantity": 2
        },
        {
            "date_time": "2015-08-24 08:45:20",
            "id": 10,
            "branch": "HEB Lincoln",
            "quantity": 2
        },
        {
            "date_time": "2015-09-08 09:04:59",
            "id": 11,
            "branch": "Soriana Palmas",
            "quantity": 2
        },
        {
            "date_time": "2015-09-22 16:21:35",
            "id": 14,
            "branch": "Grande Campestre",
            "quantity": 3
        },
        {
            "date_time": "2015-03-23 08:23:40",
            "id": 6,
            "branch": "Ocho HIdalgo",
            "quantity": 2
        }
    ],
    "entries": [
        {
            "date_time": "2015-11-18 17:29:33",
            "id": 1483,
            "branch": "Grande Campestre",
            "quantity": 2
        },
        {
            "date_time": "2015-07-03 15:50:33",
            "id": 488,
            "branch": "Ocho HIdalgo",
            "quantity": 3
        },
        {
            "date_time": "2015-07-23 11:26:14",
            "id": 558,
            "branch": "Ocho HIdalgo",
            "quantity": 1
        }
    ]
}
'''
