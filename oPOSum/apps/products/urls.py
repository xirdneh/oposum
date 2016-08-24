from django.conf.urls import include, url
from django.views.generic import TemplateView
from oPOSum.apps.products import views as products_views

urlpatterns = [
    url(r'^add-products/(?P<prod>[\-a-zA-Z0-9\.]+)?/?$', products_views.add_products, name="products-add_products"),
    url(r'^edit-products/?$', products_views.edit_products, name="products-add_products"),
    url(r'^add-category/?$', products_views.add_category, name="products-add_category"),
    url(r'^edit-category/?$', products_views.edit_category, name="products-add_category"),
    url(r'^add-provider/?$', products_views.add_provider, name="products-add_provider"),
    url(r'^edit-provider/?$', products_views.edit_provider, name="products-add_provider"),
    url(r'^get-product/(?P<slug>[\-a-zA-Z0-9\.]+)/?$', products_views.get_product, name="products-get_product"),
    url(r'^migrate-prod/?$', products_views.migrate_prod, name="products-migrate_product"),
    url(r'^get-transactions/(?P<slug>[\-a-zA-Z0-9\.]+)/?$', products_views.get_transactions, name="products-get_transactions"),
    url(r'^show-transactions/(?P<slug>[\-a-zA-Z0-9\.]+)/?$', products_views.show_transactions, name="products-show_transactions"),
    url(r'^search/?$', products_views.search, name="products-search"),
]
