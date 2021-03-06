from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from oPOSum.apps.authentication import views as auth_views


urlpatterns = [
    # Examples:
    # url(r'^oPOSum/', include('oPOSum.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/?$', auth_views.login_user, name="login"),
    url(r'^logout/?$', auth_views.logout_user, name="logout"),
    url(r'^products/', include('oPOSum.apps.products.urls')),
    url(r'^layaway/', include('oPOSum.apps.layaway.urls')),
    url(r'^pos/', include('oPOSum.apps.pos.urls')),
    url(r'^inventory/', include('oPOSum.apps.inventory.urls')),
    url(r'^clients/', include('oPOSum.apps.client.urls')),
]

from django.conf.urls.static import static
if settings.DEBUG == True:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
