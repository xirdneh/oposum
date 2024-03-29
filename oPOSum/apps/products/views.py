from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q
from oPOSum.apps.products.forms import *
from oPOSum.apps.products.models import *
from oPOSum.apps.branches.models import Branch
from oPOSum.libs import utils as pos_utils
from oPOSum.libs import products as prod_utils
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
import logging
import oPOSum.libs.migrate as migrate
import oPOSum.libs.products as prodlib
from decimal import Decimal
# Create your views here.
from django.template import RequestContext
logger = logging.getLogger("oPOSum.products")
@login_required
def add_products(request, prod = ''):
    if request.method == 'POST':
        p = Product.objects.filter(slug = request.POST['slug'].replace("-",""))
        if p:
            form = ProductForm(instance=p[0])
            if not request.is_ajax():
                return render(request, 'products/edit_products.html', { 'edit_form' : form, 'message': 'Este articulo ya existe, desea sobreescribir los datos?'})
            else:
                return HttpResponse("{ \"status\":\"ok\", \"message\":\"message\"}", content_type='application/json')
        else:
            form = ProductForm(request.POST)
        if form.is_valid(): 
            p_new = form.save()
            if not request.is_ajax():
                return render(request, 'products/add_products.html', { 'add_form' : ProductForm(), 'message':'Articulo guardado exitosamente, ' + p_new.slug})
            else:
                return HttpResponse("{ \"status\":\"ok\", \"message\":\"message\"}", content_type='application/json')
        else:
            if not request.is_ajax():
                return render(request, 'products/add_products.html', { 'add_form' : ProductForm(request.POST), 'form_errors' : form.errors})
            else:
                return HttpResponse("{ \"status\":\"error\", \"message\":\"message\"}", content_type='application/json')
    else:
        if prod == '' or not prod:
            form = ProductForm()
            return render(request, 'products/add_products.html', { 'add_form' : form })
        else:
            logger.debug("Analaizando nuevo producto: {0}".format(prod))
            return render(request, 'products/add_products.html', 
                                  { 'add_form' : ProductForm(initial= __get_full_product(prod)),
                                    'message': 'Al guardar el articulo esta ventana se cerrara',
                                    'close_on_save':True
                                  })


@login_required
def edit_products(request):
    if request.method == 'POST':
        p = Product.objects.filter( slug = request.POST['slug'])
        if p:
            form = ProductForm(request.POST, instance=p[0])
            if form.is_valid():
                p_new = form.save()
                return render(request, 'products/add_products.html', { 'add_form' : ProductForm(), 'message':'Producto editado con exito ' + p_new.slug})

    return render(request, 'products/add_products.html', { 'add_form' : ProductForm()})

@login_required
def add_category(request): 
    if request.method == 'POST':
        c = ProductCategory.objects.filter(name = request.POST['name'])
        if c:
            form = ProductCategoryForm(instance=c[0])
            return render(request, 'products/edit_category.html', { 'edit_form' : form, 'message': 'Esta categoria ya existe, desea sobreescribir los datos?'}) 
        else:
            form = ProductCategoryForm(request.POST)
        if form.is_valid(): 
            c_new = form.save()
            return render(request, 'products/add_category.html', { 'add_form' : ProductCategoryForm(), 'message':'Categoria guardado exitosamente, ' + c_new.name})
        else:
            return render(request, 'products/add_category.html', { 'add_form' : ProductCategoryForm(), 'form_errors' : form.errors})
    else:
        form = ProductCategoryForm()
        return render(request, 'products/add_category.html', { 'add_form' : form })

@login_required
def edit_category(request):
    if request.method == 'POST':
        c = ProductCategory.objects.filter( name = request.POST['name'])
        if c:
            form = ProductCategoryForm(request.POST, instance=c[0])
            if form.is_valid():
                c_new = form.save()
                return render(request, 'products/add_category.html', { 'add_form' : ProductCategoryForm(), 'message':'Categoria editada con exito ' + c_new.name})

    return render(request, 'products/add_category.html', { 'add_form' : ProductCategoryForm()})

@login_required
def add_provider(request): 
    if request.method == 'POST':
        p = Provider.objects.filter(sku = request.POST['sku'])
        if p:
            form = ProviderForm(instance=p[0])
            return render(request, 'products/edit_provider.html', { 'edit_form' : form, 'message': 'Este proveedor ya existe, desea sobreescribir los datos?'}) 
        else:
            form = ProviderForm(request.POST)
        if form.is_valid(): 
            p_new = form.save()
            return render(request, 'products/add_provider.html', { 'add_form' : ProviderForm(), 'message':'Proveedor guardado exitosamente, ' + p_new.name})
        else:
            return render(request, 'products/add_provider.html', { 'add_form' : ProviderForm(), 'form_errors' : form.errors})
    else:
        form = ProviderForm()
        return render(request, 'products/add_provider.html', { 'add_form' : form })

@login_required
def edit_provider(request):
    if request.method == 'POST':
        p = Provider.objects.filter( sku = request.POST['sku'])
        if p:
            form = ProviderForm(request.POST, instance=p[0])
            if form.is_valid():
                p_new = form.save()
                return render(request, 'products/add_provider.html', { 'add_form' : ProviderForm(), 'message':'Proveedor modificado exitosamente ' + p_new.name})
    return render(request, 'products/add_provider.html', { 'add_form' : ProviderForm()})

@login_required
def get_product(request, slug):
    slug = slug
    logger.debug("Buscando producto con slug: {0}".format(slug))
    try:
        p = Product.objects.get(slug=slug.replace("-",""))
    except Product.DoesNotExist:
        #logger.debug("No conocemos el product: {0}".format(slug));
        #p = migrate.get_art(slug.replace("-", "")) 
        #if len(p) > 0 :
        #    p = migrate.get_migration_details( p[0][15], p[0][1] ) 
        #    logger.error("Producto desconocido: {0}".format(p))
        #    ret = {
        #        'status':'ok',
        #        'message': 'Migrando',
        #        'product':p
        #        }
        #else:
        logger.error("Producto no encontrado")
        ret = {}
        ret['status'] = 'error'
        ret['message'] = 'Producto no encontrado'
        ret['slug'] = slug
        return HttpResponse(json.dumps(ret) , content_type='application/json')
    logger.debug('Producto conocido')
    if p.regular_price == Decimal('0.00') and p.line is not None:
        retail_price = p.equivalency * p.line.price
    else:
        retail_price = p.regular_price
    desc = prod_utils.get_discounts(p)
    des = {'discount': '0'}
    if desc is not None and desc and desc:
        try:
            des = {'discount': desc.slug[-2:] }
        except:
            des = {'discount': '0'}
    ret = {
        'status':'ok',
        'message': 'Existente',
        'product': 
            {
                'slug':p.slug, 
                'price':str(p.regular_price), 
                'description':p.description,
                'retail_price':str(round(retail_price,2))
            },
        'desc': des
    }
    logger.debug("Producto conocido: {0}".format(p))
    return HttpResponse(json.dumps(ret) , content_type='application/json')

def __get_full_product(slug):
    try:
        p = Product.objects.get(slug = slug.replace("-", ""))
        initial= { 
           'slug': p.slug,
           'provider': p.provider ,
           'category': [c.id for c in p.category.all()],
           'line': p.line,
           'regular_price': p.regular_price,
           'equivalency': p.equivalency ,
           'description':p.description,
           'close_after': True,
           }
    except Product.DoesNotExist:
        p_det = migrate.get_migration_details(slug, '')
        product = prodlib.check_product(p_det)
        initial= { 
           'slug': product['code'],
           'provider':product['prov'] ,
           'category': [product['bodega'], product['area'], product['linea'], product['marca']],
           'line':product['line'] ,
           'regular_price': product['regular_price'],
           'equivalency':product['equivalency'] ,
           'description':'',
           'close_after': True
           }

    return initial

@login_required
def migrate_prod(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        json_p = data['product']
        product = prodlib.verify_product(json_p)
        p = product['obj']
        ret = {
            'status': 'ok',
            'message': 'Ok',
            'product': {
                        'slug':p.slug,
                        'price':str(p.regular_price),
                        'description':p.description
                        }
        }
        return HttpResponse(json.dumps(ret), content_type='application/json')

@login_required
def get_transactions(request, slug):
    p = Product.objects.get(slug = slug.replace('-', ''))
    return HttpResponse("{\"response\": \"ok\", \"result\":" + json.dumps(p.get_transactions()) + "}", content_type="application/json");

@login_required
def show_transactions(request, slug):
    p = Product.objects.get(slug = slug.replace('-', ''))
    transactions = p.get_transactions()
    return render(request, 'products/show_transactions.html', { 'transactions' : transactions, 'product' : p, 'product_cats': p.category.all()})

@login_required
def search(request):
    q = request.GET['q']
    ps = Product.objects.filter(Q(slug__icontains=q) | Q(name__icontains=q)).order_by('slug')
    ret = []
    for p in ps:
        ret.append({
            'slug': p.slug,
            'name': p.name,
            'description': p.description,
            'existence': p.get_transactions_count()
        })
    ret = sorted(ret, key=lambda o: o['existence'], reverse=True)
    return render(request, 'products/search.html', { 'products' : ret})

