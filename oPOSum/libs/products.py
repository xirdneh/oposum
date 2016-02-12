from oPOSum.apps.products.models import *
from django.core.exceptions import ObjectDoesNotExist
import sys
import MySQLdb as mdb
import logging
from decimal import Decimal
import pytz
from datetime import datetime
logger = logging.getLogger(__name__)

def verify_product(prod):
    product = {}
    product['is_watch'] = False;
    product['is_weight'] = False;
    product['is_price'] = False;
    if prod['linea'] == 25 or prod['linea'] == 17 or prod['linea'] == 13:
        products['is_watch'] = True;
        try:
            marca = ProductCategory.objects.get(slug = prod['prov'], type = 'marca')
        except ProductCategory.DoesNotExist:
            marca = ProductCategory(slug = prod['prov'], type= 'marca', name = prod['prov'])
            marca.save()
            logger.debug("Marca creada: {0}".format(marca))
    else:
        try:
            prov = Provider.objects.get(sku = prod['prov'])
        except Provider.DoesNotExist:
            prov = Provider( sku = prod['prov'],
                             name = prod['prov'])
            prov.save()
            logger.debug("Prov creado: {0}".format(prov))
    try:
        bodega = ProductCategory.objects.get(slug = prod['bodega'], type = 'bodega')
    except ProductCategory.DoesNotExist:
        bodega = ProductCategory(slug = prod['bodega'], type = 'bodega', name = prod['bodega'])
        bodega.save()
        logger.debug("Bodega creada: {0}".format(bodega))
    try:
        area = ProductCategory.objects.get(slug = prod['area'], type = 'area')
    except ProductCategory.DoesNotExist:
        area = ProductCategory(slug = prod['area'], type='area', name=prod['area'])
        area.save()
        logger.debug("Area creada: {0}".format(area))
    try:
        linea = ProductCategory.objects.get(slug = prod['linea'], type = 'linea')
    except ProductCategory.DoesNotExist:
        linea = ProductCategory(slug = prod['linea'], type = 'linea', name = prod['linea'])
        linea.save()
        logger.debug("Linea creada: {0}".format(linea))
    if prod['line'] != '':
        product['is_weight'] = True;
        if bodega.slug == "1":
            lt = "10k"
        elif bodega.slug == "2":
            lt = "14k"
        elif bodega.slug == "16":
            lt = "plata"
        try:
            line = ProductLine.objects.get(name = prod['line'], type = lt)
        except ProductLine.DoesNotExist:
            line = ProductLine(name = prod['line'], price = Decimal('0.0'))
            line.save()
            logger.debug("Line creada: {0}".format(line))
    if prod['price'] != '0.0':
        product['is_price'] = True;
    p = Product.objects.create(slug = prod['code'], provider = prov, name = prod['name'], description = prod['description'])
    p.category.add(bodega)
    p.category.add(area)
    p.category.add(linea)
    if product['is_watch']:
        p.category.add(marca)
    if product['is_weight']:
        p.line = line
        p.equivalency = Decimal(prod['equivalency'])
    if product['is_price']:
        p.regular_price = Decimal(prod['price'])
    p.save()
    logger.debug("Producto creado: {0}".format(p))
    product['obj'] = p
    return product

def check_product(prod):
    product = {}
    product['is_watch'] = False;
    product['is_weight'] = False;
    product['is_price'] = False;
    product['prov'] = 0
    product['marca'] = 0
    if prod['linea'] == 25 or prod['linea'] == 17 or prod['linea'] == 13:
        products['is_watch'] = True;
        try:
            product['marca'] = ProductCategory.objects.get(slug = prod['prov'], type = 'marca').id
        except ProductCategory.DoesNotExist:
            product['marca'] = 0
    else:
        try:
            product['prov'] = Provider.objects.get(sku = prod['prov']).id
        except Provider.DoesNotExist:
            product['prov'] = 0
    try:
        product['bodega'] = ProductCategory.objects.get(slug = prod['bodega'], type = 'bodega').id
    except ProductCategory.DoesNotExist:
            product['bodega'] = 0
    try:
        product['area'] = ProductCategory.objects.get(slug = prod['area'], type = 'area').id
    except ProductCategory.DoesNotExist:
        product['area'] = 0
    try:
        product['linea'] = ProductCategory.objects.get(slug = prod['linea'], type = 'linea').id
    except ProductCategory.DoesNotExist:
        product['linea'] = 0
    if prod['line'] != '':
        product['is_weight'] = True;
        if product['bodega'] == 1:
            product['lt'] = "10k"
        elif product['bodega'] == 2:
            product['lt'] = "14k"
        else:
            product['lt'] = ""
        try:
            product['line'] = ProductLine.objects.get(name = prod['line'], type = product['lt']).id
        except ProductLine.DoesNotExist:
            product['line'] = 0
    else:
        product['line'] = prod['line']
    if prod['price'] != '0.0':
        product['is_price'] = True;
    product['code'] = prod['name']
    product['equivalency'] = prod['equivalency']
    product['regular_price'] = prod['price']
    return product

def get_discounts(p):
    utc = pytz.timezone('UTC')
    dtu = datetime.utcnow()
    dt = dtu.replace(tzinfo = utc)
    tz = pytz.timezone('America/Monterrey')
    dt = dt.astimezone(tz)
    desc = False
    slug = False
    if( datetime(2016, 2, 1, 0, 0, 0, 0, tz) <= dt and
        datetime(2016, 2, 29, 23, 59, 0, 0, tz) >= dt ):
        if (p.provider.sku == '81' or p.prodiver.sku == '91'):
            slug = 'DICDESC50'
        if slug:
            desc = Product.objects.get(slug = slug)
        return desc
    return False  
