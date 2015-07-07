from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.client.views',
    url(r'^$', 'index', name='client-index'),
    url(r'new/?(?P<client_id>[0-9]+)?$', 'new', name='client-new'),
    url(r'search/?$', 'search', name='client-search'),
    )
