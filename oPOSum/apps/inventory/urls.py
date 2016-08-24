from django.conf.urls import include, url
from oPOSum.apps.inventory import views as inventory_views

urlpatterns = [
    url(r'^entries/?$', inventory_views.entries, name="inventory-entries"),
    url(r'^manage-entries/?$', inventory_views.manage_entries, name="manage-entries"), 
    url(r'^manage-exits/?$', inventory_views.manage_exits, name="manage-exits"), 
    url(r'^inventory-check/?$', inventory_views.inventory_check, name="inventory-check"),
    url(r'^save-entry/?$', inventory_views.save_entry, name="inventory_save-entry"),
    url(r'^delete-entry/?$', inventory_views.delete_entry, name="inventory_delete-entry"),
    url(r'^update-entry/?$', inventory_views.update_entry, name="inventory_update-entry"),
    url(r'^current-inventory/?$', inventory_views.current_inventory, name="current-inventory"),
    url(r'^save-entries/?$', inventory_views.save_entries, name="inventory_save-entries"),
    url(r'^save-exits/?$', inventory_views.save_exits, name="inventory_save-entries"),
    url(r'^print-entries-report/(?P<id>[0-9]+)/?$', inventory_views.print_entries_report, name="inventory_print-entries-report"),
    url(r'^print-exits-report/(?P<id>[0-9]+)/?$', inventory_views.print_exits_report, name="inventory_print-entries-report"),
    url(r'^existence-history/(?P<id>[0-9]+)/?$', inventory_views.existence_history, name="inventory_existence-history"),
    url(r'^adjustments-inventory/?$', inventory_views.adjustments_inventory, name="inventory_adjustments-inventory"),
    url(r'^get-adjustments/(?P<id>[0-9]+)/?$', inventory_views.get_adjustments, name="inventory_get-adjustments"),
    url(r'^save-adjustments/?$', inventory_views.save_adjustments, name="inventory_save-adjustments"),
    url(r'^print-inventory-existence(/(?P<id>[0-9]+))?/?$', inventory_views.print_inventory_existence, name="inventory_print-inventory_existence"),
    url(r'^print-inventory-surplus/?$', inventory_views.print_inventory_surplus, name="inventory_print-inventory_surplus"),
    url(r'^print-inventory-missing/?$', inventory_views.print_inventory_missing, name="inventory_print-inventory_missing"),
    url(r'^transfers/save-transfer/?$', inventory_views.save_transfer, name="products-save_transfer"),
    url(r'^transfers/accept-transfer/(?P<id>[0-9]+)/?$', inventory_views.accept_transfer, name="products-accept_transfer"),
    url(r'^transfers/(?P<branch>[\-a-zA-Z0-9\.]+)?/?$', inventory_views.transfers, name="products-transfers"),
]
