from django.contrib import admin
from oPOSum.apps.pos.models import *

# Register your models here.
admin.site.register(Sale)
#admin.site.register(Layaway)
#admin.site.register(LayawayHistory)
admin.site.register(SaleDetails)
admin.site.register(POSFolio)
