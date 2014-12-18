from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from oPOSum.apps.products.forms import *
from oPOSum.apps.products.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
# Create your views here.
from django.template import RequestContext
@login_required
def add_products(request):
    if request.method == 'POST':
        p = Product.objects.filter(slug = request.POST['slug'])
        if p:
            form = ProductForm(instance=p[0])
            return render_to_response('products/edit_products.html', { 'edit_form' : form, 'message': 'Este articulo ya existe, desea sobreescribir los datos?'}, context_instance=RequestContext(request)) 
        else:
            form = ProductForm(request.POST)
        if form.is_valid(): 
            p_new = form.save()
            return render_to_response('products/add_products.html', { 'add_form' : ProductForm(), 'message':'Articulo guardado exitosamente, ' + p_new.slug}, context_instance=RequestContext(request))
        else:
            return render_to_response('products/add_products.html', { 'add_form' : ProductForm(), 'form_errors' : form.errors}, context_instance=RequestContext(request))
    else:
        form = ProductForm()
        return render_to_response('products/add_products.html', { 'add_form' : form }, context_instance=RequestContext(request))

@login_required
def edit_products(request):
    if request.method == 'POST':
        p = Product.objects.filter( slug = request.POST['slug'])
        if p:
            form = ProductForm(request.POST, instance=p[0])
            if form.is_valid():
                p_new = form.save()
                return render_to_response('products/add_products.html', { 'add_form' : ProductForm(), 'message':'Producto editado con exito ' + p_new.slug}, context_instance=RequestContext(request))
    return render_to_response('products/add_products.html', { 'add_form' : ProductForm()}, context_instance=RequestContext(request))

@login_required
def add_category(request): 
    if request.method == 'POST':
        c = ProductCategory.objects.filter(name = request.POST['name'])
        if c:
            form = ProductCategoryForm(instance=c[0])
            return render_to_response('products/edit_category.html', { 'edit_form' : form, 'message': 'Esta categoria ya existe, desea sobreescribir los datos?'}, context_instance=RequestContext(request)) 
        else:
            form = ProductCategoryForm(request.POST)
        if form.is_valid(): 
            c_new = form.save()
            return render_to_response('products/add_category.html', { 'add_form' : ProductCategoryForm(), 'message':'Categoria guardado exitosamente, ' + c_new.name}, context_instance=RequestContext(request))
        else:
            return render_to_response( 'products/add_category.html', { 'add_form' : ProductCategoryForm(), 'form_errors' : form.errors}, context_instance=RequestContext(request))
    else:
        form = ProductCategoryForm()
        return render_to_response('products/add_category.html', { 'add_form' : form }, context_instance=RequestContext(request))

@login_required
def edit_category(request):
    if request.method == 'POST':
        c = ProductCategory.objects.filter( name = request.POST['name'])
        if c:
            form = ProductCategoryForm(request.POST, instance=c[0])
            if form.is_valid():
                c_new = form.save()
                return render_to_response(request, 'products/add_category.html', { 'add_form' : ProductCategoryForm(), 'message':'Categoria editada con exito ' + c_new.name})
    return render_to_response('products/add_category.html', { 'add_form' : ProductCategoryForm()}, context_instance=RequestContext(request))

@login_required
def add_provider(request): 
    if request.method == 'POST':
        p = Provider.objects.filter(sku = request.POST['sku'])
        if p:
            form = ProviderForm(instance=p[0])
            return render_to_response('products/edit_provider.html', { 'edit_form' : form, 'message': 'Este proveedor ya existe, desea sobreescribir los datos?'}, context_instance=RequestContext(request)) 
        else:
            form = ProviderForm(request.POST)
        if form.is_valid(): 
            p_new = form.save()
            return render_to_response('products/add_provider.html', { 'add_form' : ProviderForm(), 'message':'Proveedor guardado exitosamente, ' + p_new.name}, context_instance=RequestContext(request))
        else:
            return render_to_response('products/add_provider.html', { 'add_form' : ProviderForm(), 'form_errors' : form.errors}, context_instance=RequestContext(request))
    else:
        form = ProviderForm()
        return render_to_response('products/add_provider.html', { 'add_form' : form }, context_instance=RequestContext(request))

@login_required
def edit_provider(request):
    if request.method == 'POST':
        p = Provider.objects.filter( sku = request.POST['sku'])
        if p:
            form = ProviderForm(request.POST, instance=p[0])
            if form.is_valid():
                p_new = form.save()
                return render_to_response('products/add_provider.html', { 'add_form' : ProviderForm(), 'message':'Proveedor modificado exitosamente ' + p_new.name}, context_instance=RequestContext(request))
    return render_to_response('products/add_provider.html', { 'add_form' : ProviderForm()}, context_instance=RequestContext(request))

@login_required
def get_product(request, slug):
    try:
        p = Product.objects.get(slug=slug)
        ret = []
        ret.append({'slug':p.slug, 'price':str(p.regular_price), 'description':p.description})
    except Product.DoesNotExist:
        ret = []
    return HttpResponse(json.dumps(ret) , mimetype='application/json')
