from django.conf.urls import include, url
from oPOSum.apps.layaway import views as layaway_views

urlpatterns = [
    url(r'save-layaway/?$', layaway_views.save_layaway, name='layaway-save'),
    url(r'save-payment/?$', layaway_views.save_payment, name='layaway-payment'),
    url(r'unpaid-layaways/?$', layaway_views.get_unpaid_layaways, name='unpaid-layaways'),
    url(r'$', layaway_views.index, name='layaway-index'),
] 
