from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.inventory.views',
    url(r'^entries/?$', 'entries', name="inventory-entries"),
)
