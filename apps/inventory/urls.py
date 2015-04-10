from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.inventory.views',
    url(r'^entries/?$', 'entries', name="inventory-entries"),
    url(r'^manage-entries/?$', 'manage_entries', name="manage-entries"), 
    url(r'^manage-exits/?$', 'manage_exits', name="manage-exits"), 
    url(r'^inventory-check/?$', 'inventory_check', name="inventory-check"),
    url(r'^save-entry/?$', 'save_entry', name="inventory_save-entry"),
    url(r'^delete-entry/?$', 'delete_entry', name="inventory_delete-entry"),
    url(r'^current-inventory/?$', 'current_inventory', name="current-inventory"),
    url(r'^save-entries/?$', 'save_entries', name="inventory_save-entries"),
    url(r'^save-exits/?$', 'save_exits', name="inventory_save-entries"),
    url(r'^print-entries-report/(?P<id>[0-9]+)/?$', 'print_entries_report', name="inventory_print-entries-report"),
    url(r'^print-exits-report/(?P<id>[0-9]+)/?$', 'print_exits_report', name="inventory_print-entries-report"),
    url(r'^existence-history/(?P<id>[0-9]+)/?$', 'existence_history', name="inventory_existence-history"),
)
