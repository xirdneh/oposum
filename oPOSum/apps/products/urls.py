from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from oPOSum.apps.products.views import *

urlpatterns = patterns('oPOSum.apps.products.views',
    url(r'^add-products/(?P<prod>[\-a-zA-Z0-9\.]+)?/?$', 'add_products', name="products-add_products"),
    url(r'^edit-products/?$', 'edit_products', name="products-add_products"),
    url(r'^add-category/?$', 'add_category', name="products-add_category"),
    url(r'^edit-category/?$', 'edit_category', name="products-add_category"),
    url(r'^add-provider/?$', 'add_provider', name="products-add_provider"),
    url(r'^edit-provider/?$', 'edit_provider', name="products-add_provider"),
    url(r'^get-product/(?P<slug>[\-a-zA-Z0-9\.]+)/?$', 'get_product', name="products-get_product"),
    url(r'^migrate-prod/?$', 'migrate_prod', name="products-migrate_product"),
    url(r'^get-transactions/(?P<slug>[\-a-zA-Z0-9\.]+)/?$', 'get_transactions', name="products-get_transactions"),
)
