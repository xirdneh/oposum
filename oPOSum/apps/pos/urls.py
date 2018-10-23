from django.conf.urls import include, url
from oPOSum.apps.pos import views as pos_views

urlpatterns = [
    url(r'^sales/?$', pos_views.sales, name="pos-sales"),
    url(r'^mock-sales/?$', pos_views.mock_sales, name="pos-sales"),
    url(r'^save-sale/?$', pos_views.save_sale, name="pos-save_sale"),
    url(r'^mock-sale/?$', pos_views.mock_sale, name="pos-save_sale"),
    url(r'^pos-folio/(?P<branch>[\w-]+)/(?P<type>\w+)/?', pos_views.get_pos_folio, name="pos-pos_folio"),
    url(r'^report-sales/(?P<branch>[\w-]+)/(?P<urldatetime>[\w-]+)?/?', pos_views.get_sales_report, name="pos-sales_report"),
    url(r'^report-sales-branch/(?P<branch>[\w-]+)/(?P<datestart>[\w-]+)(?:/(?P<dateend>[\w-]+))?/?', pos_views.get_sales_report_branch, name="pos-sales-report-branch"),
]
