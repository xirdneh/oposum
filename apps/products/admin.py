from django.contrib import admin
from oPOSum.apps.products.models import *
# Register your models here.

class ProductCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'type')
        }),
        ('Details',  {
            'fields': ('parent', 'description')
        }),
    )
    list_display = ('name', 'slug', 'type')
    list_filter = ('type',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'provider')
    list_filter = ('provider',)
    search_fields = ['slug', 'name']
    filter_horizontal = ['category']


admin.site.register(ProviderDetail)
admin.site.register(Provider)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductLine)
admin.site.register(ProductDetail)
admin.site.register(Product, ProductAdmin)
