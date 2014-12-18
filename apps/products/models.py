from django.db import models
from django.utils.translation import ugettext as _
from decimal import *

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
