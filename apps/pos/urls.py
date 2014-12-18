from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.pos.views',
    url(r'^sales/?$', 'sales', name="pos-sales"),
    url(r'^save-sale/?$', 'save_sale', name="pos-save_sale"),
    url(r'^pos-folio/(?P<branch>[\w-]+)/(?P<type>\w+)/?', 'get_pos_folio', name="pos-pos_folio"),
    url(r'^report-sales/(?P<branch>[\w-]+)/(?P<urldatetime>[\w-]+)/?', 'get_sales_report', name="pos-sales_report"),
)
