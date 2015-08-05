from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.client.views',
    url(r'^$', 'index', name='client-index'),
    url(r'new/?^$', 'new', name='client-new'),
    url(r'search/?^$', 'search', name='client-search'),
    )
