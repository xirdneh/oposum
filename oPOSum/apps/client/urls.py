from django.conf.urls import include, url
from oPOSum.apps.client import views as client_views

urlpatterns = [
    url(r'^$', client_views.index, name='client-index'),
    url(r'new/?(?P<client_id>[0-9]+)?$', client_views.new, name='client-new'),
    url(r'search/?$', client_views.search, name='client-search'),
] 
