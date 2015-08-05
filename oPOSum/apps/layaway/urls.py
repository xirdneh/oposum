from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.layaway.views',
    url(r'save-layaway/?$', 'save_layaway', name='layaway-save'),
    url(r'save-payment/?$', 'save_payment', name='layaway-payment'),
    url(r'$', 'index', name='layaway-index'),
    )
