from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.layaway.views',
    url(r'^$', 'index', name='layaway-index'),
    )
