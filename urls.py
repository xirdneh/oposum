from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^oPOSum/', include('oPOSum.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/?$', 'oPOSum.apps.authentication.views.login_user', name="login"),
    url(r'^logout/?$', 'oPOSum.apps.authentication.views.logout_user', name="logout"),
    url(r'^products/', include('oPOSum.apps.products.urls')),
    url(r'^pos/', include('oPOSum.apps.pos.urls')),
    url(r'^inventory/', include('oPOSum.apps.inventory.urls')),
)
