from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from oPOSum.apps.products.models import *
from django.utils.translation import ugettext as _

class ProductForm(forms.ModelForm):
    close_after = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=False)
    class Meta:
        model = Product
        fields = ['slug', 'name', 'provider', 'category', 'line', 'regular_price', 'equivalency', 'description']
        widgets = {
            'slug' : forms.TextInput(attrs={ 'tabindex' : 0}),
            'name' : forms.HiddenInput(),
            'provider' : forms.Select(attrs={ 'tabindex' : 1}),
            'category' : FilteredSelectMultiple('ProductCategory',False,attrs={ 'tabindex' : 2}),
            'line' : forms.Select(attrs={ 'tabindex' : 3}),
            'regular_price' : forms.NumberInput(attrs={ 'tabindex' : 4}),
            'equivalency' : forms.NumberInput(attrs={ 'tabindex': 5}),
            'description' : forms.Textarea(attrs={ 'tabindex' : 6}),
        }
        labels = {
            'provider' : 'Proveedor',
            'category' : 'Categoria',
            'line' : 'Linea',
        }
    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/static/js/jsi18n.js']
    
    def save(self, *args, **kwargs):
        self.instance.name = self.instance.slug
        self.instance.slug = self.instance.slug.replace("-", "")
        return super(ProductForm, self).save(*args, **kwargs)

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['sku', 'name', 'type', 'address', 'telephone1', 'telephone2']
        widgets = {
            'sku' : forms.TextInput(attrs ={ 'tabindex' : 0}),
            'name' : forms.TextInput(attrs = { 'tabindex' : 1}),
            'type' : forms.TextInput(attrs = { 'tabindex' : 2}),
            'address' : forms.TextInput(attrs = { 'tabindex' : 3}),
            'telephone1' : forms.TextInput(attrs = { 'tabindex' : 4}),
            'telephone2' : forms.TextInput(attrs = { 'tabindex' : 5}),
        }
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'slug', 'type']
        widgets = {
           'name' : forms.TextInput(attrs = { 'tabindex' : 0}),
           'slug' : forms.TextInput(attrs = { 'tabindex' : 1}),
           'type' : forms.Select(attrs = { 'tabindex' : 2}),
        }
        
class ProductLineForm(forms.ModelForm):
    class Meta:
        model = ProductLine
        fields = ['name', 'price', 'type'] 
        widgets = {
            'name' : forms.TextInput(attrs = { 'tabindex' : 0}),
            'slug' : forms.TextInput(attrs = { 'tabindex' : 1}),
            'type' : forms.Select(attrs = { 'tabindex' : 2 }),
        }
