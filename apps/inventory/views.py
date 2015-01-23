from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from oPOSum.apps.inventory.models import Inventory, InventoryEntry
from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from django.http import HttpResponse
import json, sys, traceback
from datetime import datetime
# Create your views here.
import logging

logger = logging.getLogger(__name__)
@login_required
def entries(request):
    pass

@login_required
def add_existence(request):
    return render_to_response('inventory/add_existence.html', 
                              context_instance=RequestContext(request))

@login_required
def inventory_check(request):
    inventory = Inventory.objects.filter(enabled = True).order_by('date_time')
    branches = list(request.user.employee.branch.all())
    if len(inventory) > 0 and inventory[0].branch in branches:
        inventory = inventory[0]
        request.session['inventory_id'] = inventory.id
        return render_to_response('inventory/inventory_check.html', { 'inventory': inventory, 'enable_form': True, 'inv_branch':inventory.branch.slug },context_instance=RequestContext(request))
    else:
        if len(inventory) < 1:
            title = 'No hay inventarios programados'
        elif not inventory[0].branch in branches:
            title = 'No hay acceso al inventario programado'
        return render_to_response('inventory/inventory_check.html', { 'title':title , 'enable_form': False },context_instance=RequestContext(request))

@login_required
def save_entry(request):
    if request.is_ajax():
        logger.debug(request.POST['data'])
        post_json = json.loads(request.POST['data'])
        user = User.objects.get(username = post_json['user'])
        slug = post_json['slug'].replace('-', '')
        product = Product.objects.get(slug=slug)
        qty = int(post_json['qty'])
        logger.debug(post_json)
        inv = request.session.get('inventory_id', False)

        if not inv:
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", mimetype="application/json")
        logger.debug("Inventory id: {0}".format(inv))
        try: 
            inventory = Inventory.objects.get(id=inv)
            try:
                inv_entry = InventoryEntry.objects.get(inv=inventory, product = product)
            except InventoryEntry.DoesNotExist:
                ie = InventoryEntry(
                            inv = inventory,
                            product = product,
                            quantity = qty,
                            user = user)
                ie.save()
                return HttpResponse("{ \"status\": \"ok\", \"message\":\"OK\"}", mimetype="application/json")
            logger.debug(inv_entry)
            inv_entry.quantity += qty
            inv_entry.date_time = datetime.now()
            inv_entry.save()
            return HttpResponse("{ \"status\": \"ok\", \"message\":\"OK\"}", mimetype="application/json")
        except:
            logger.error("Unexpected error:{0} ".format(sys.exc_info()[0]))
            logger.error("Error data: {0}".format(post_json))
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", mimetype="application/json")


@login_required
def delete_entry(request):
    if request.is_ajax():
        logger.debug(request.POST['data'])
        post_json = json.loads(request.POST['data'])
        user = User.objects.get(username = post_json['user'])
        slug = post_json['slug'].replace('-', '')
        product = Product.objects.get(slug = slug)
        qty = int(post_json['qty'])
        inv = request.session.get('inventory_id', False)
        if not inv:
            logger.error("No inventory found")
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", mimetype="application/json")
        try:
            inventory = Inventory.objects.get(id=inv)
            try:
                inv_entry = InventoryEntry.objects.get(inv=inventory, product = product)

            except InventoryEntry.DoesNotExist:
                logger.error("No entry found")
                return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", mimetype="application/json")
            logger.debug(inv_entry)
            if (inv_entry.quantity - qty) < 0:
                logger.error("Negative Quantity:{0} ".format(qty))
                return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", mimetype="application/json")
            else:
                inv_entry.quantity -= qty
                inv_entry.date_time = datetime.now()
                inv_entry.save()
                return HttpResponse("{ \"status\": \"ok\", \"message\":\"OK\"}", mimetype="application/json")
        except:
            logger.error("Unexpected error:{0} ".format(sys.exc_info()[0]))
            logger.error("Unexpected error:\n{0} ".format(traceback.format_exc()))
            logger.error("Error data: {0}".format(post_json))
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", mimetype="application/json")


@login_required
def current_inventory(request):
    inv = request.session.get('inventory_id', False)
    if not inv:
        logger.error("No inventory found")
        return render_to_response('inventory/current_inventory.html', { 'entries': [] },context_instance=RequestContext(request))
    try:
        inventory = Inventory.objects.get(id=inv)
        entries = InventoryEntry.objects.filter(inv = inventory)
        ret = [entry.as_json() for entry in entries]
        return render_to_response('inventory/current_inventory.html', { 'entries': json.dumps(ret), 'inv_branch':inventory.branch.slug, 'enable_form':True },context_instance=RequestContext(request))
    except :
        logger.error("No inventory found")
        logger.error("Unexpected error:\n{0} ".format(traceback.format_exc()))
        return render_to_response('inventory/current_inventory.html', { 'entries': [] },context_instance=RequestContext(request))

    #ret = [sale.as_json() for sale in sales]
