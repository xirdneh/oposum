from django.contrib import admin
from oPOSum.apps.inventory.models import *
# Register your models here.

class InventoryEntryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('inv', 'product', 'quantity', 'user')
        }),
    )
    list_display = ('inv', 'product', 'quantity', 'user', 'date_time')
    list_filter = ('inv', )
    search_fields = ['inv', 'product']

class ExistenceAdmin(admin.ModelAdmin):
    list_display = ('branch', 'product', 'quantity', 'date_time')
    list_filter = ('branch', )
    search_fields = ['branch', 'product']

admin.site.register(Existence, ExistenceAdmin)
admin.site.register(ExistenceHistory)
#admin.site.register(Client)
admin.site.register(ExistenceHistoryDetail)
admin.site.register(Inventory)
admin.site.register(InventoryEntry, InventoryEntryAdmin)
admin.site.register(ProductTransfer)
admin.site.register(ProductTransferDetail)
admin.site.register(ProductTransferHistory)
