from django.contrib import admin
from oPOSum.apps.inventory.models import *
# Register your models here.

admin.site.register(Existence)
admin.site.register(ExistenceHistory)
admin.site.register(Client)
admin.site.register(ExistenceHistoryDetail)
admin.site.register(InventoryFolio)
