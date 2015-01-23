from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.inventory.views',
    url(r'^entries/?$', 'entries', name="inventory-entries"),
    url(r'^add-existence/?$', 'add_existence', name="add-existence"), 
    url(r'^inventory-check/?$', 'inventory_check', name="inventory-check"),
    url(r'^save-entry/?$', 'save_entry', name="inventory_save-entry"),
    url(r'^delete-entry/?$', 'delete_entry', name="inventory_delete-entry"),
    url(r'^current-inventory/?$', 'current_inventory', name="current-inventory"),
)
