from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from oPOSum.apps.inventory.models import *
from oPOSum.apps.products.models import Product
from oPOSum.apps.branches.models import Branch
from django.contrib.auth.models import User
from django.http import HttpResponse
import json, sys, traceback, pytz
from datetime import datetime
from oPOSum.libs.reporter import PDFReporter
from pytz import timezone
import pytz
# Create your views here.
import logging

logger = logging.getLogger(__name__)
@login_required
def entries(request):
    return render_to_response('inventory/entries.html', context_instance=RequestContext(request))

@login_required
def manage_existence(request):
    return render_to_response('inventory/add_existence.html', 
                              context_instance=RequestContext(request))
@login_required
def manage_entries(request):
    return render_to_response('inventory/add_existence.html', 
                              context_instance=RequestContext(request))
@login_required
def manage_exits(request):
    return render_to_response('inventory/add_exits.html', 
                              context_instance=RequestContext(request))

@login_required
def save_entries(request):
    data = json.loads(request.POST['data'])
    logger.debug("Data to save for entries: {0}".format(data))
    u = User.objects.get(username = data['user'])
    b = Branch.objects.get(slug = data['branch'])
    details = data['details']
    msg = data['detmsg']
    try:
        eh = ExistenceHistory(user = u, branch = b, action = 'altas')
        if msg is not None and msg != '':
            eh.details = msg
        eh.save();
        for d in details:
            p = Product.objects.get(slug = d['slug'].replace('-', ''))
            q = int(d['qty'])
            try:
                e = Existence.objects.get(branch = b, product = p)
            except Existence.DoesNotExist:
                logger.debug("Creating Existence for {0}".format(b.name))
                e = Existence(product = p, quantity = 0, branch = b)
            e.quantity += q
            e.save()
            logger.debug("Existence saved: {0}".format(e))
            try:
                ehd = ExistenceHistoryDetail.objects.get(product = p, existence = eh)
                ehd.quantity += q
            except ExistenceHistoryDetail.DoesNotExist:
                ehd = ExistenceHistoryDetail(product = p, quantity = q, existence = eh)
            ehd.save()
    except:
        logger.debug("Error while saving entries history \n{0}".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"error\", \"message\":\"\"}", content_type="application/json")
    return HttpResponse("{ \"status\": \"ok\", \"folio\":\"" + str(eh.id) + "\"}", content_type="application/json")

@login_required
def save_exits(request):
    data = json.loads(request.POST['data'])
    u = User.objects.get(username = data['user'])
    b = Branch.objects.get(slug = data['branch'])
    details = data['details']
    msg = data['detmsg']
    existence = []
    existence_errors = []
    isFine = True
    try:
        eh = ExistenceHistory(user = u, branch = b, action = 'bajas')
        if msg is not None and msg != '':
            eh.details = msg
        for d in details:
            p = Product.objects.get(slug = d['slug'].replace('-', ''))
            q = int(d['qty'])
            try:
                e = Existence.objects.get(branch = b, product = p)
                #if(isFine and e.product.get_branch_transactions_count(b) >= q):
                existence.append((p, 'fine', q, e))
                #else:
                #    isFine = False
                #    if(e.product.get_branch_transactions_count(b) < q):
                #        existence_errors.append((e.product.name, 'qty', e.product.get_branch_transactions_count(b)))
            except Existence.DoesNotExist:
                entries = ExistenceHistoryDetail.object.fitler(product = p, 
                                       existence__branch = b, existence__action = 'altas')
                if len(entries) > 0:
                    isFine = True
                else:
                    isFine = False
                    existence_errors.append((p.name, 'exist', 0))
        if isFine:
            eh.save();
            for p in existence:
                try:
                    ehd = ExistenceHistoryDetail.objects.get(product = p[0], existence = eh)
                    ehd.quantity += p[2]
                except ExistenceHistoryDetail.DoesNotExist:
                    ehd = ExistenceHistoryDetail(product = p[0], quantity = p[2], existence = eh)
                ehd.save()
        else:
            logger.debug("Error while saving exits history \n{0}".format(traceback.format_exc()))
            error = """{{ \"status\": \"error\", 
                                 \"message\":\"\", 
                                 \"products\":{0}}}
                    """.format(json.dumps(existence_errors))
            return HttpResponse(error,
                                content_type="application/json")

    except:
        logger.debug("Error while saving exits history \n{0}".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"error\", \"message\":\"\"}", content_type="application/json")
    return HttpResponse("{ \"status\": \"ok\", \"folio\":\"" + str(eh.id) + "\"}", content_type="application/json")

@login_required
def print_exits_report(request, id):
    logger.debug("Creating Report for: {0}".format(id))
    try:
        dt_now = datetime.utcnow().replace(tzinfo = pytz.utc)
        eh = ExistenceHistory.objects.get(id = id)
        ehds = ExistenceHistoryDetail.objects.filter(existence = eh).order_by('product__name')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename=Reporte_Entradas_' + eh.branch.name + '_' + eh.date_time.strftime('%d-%b-%Y') + '.pdf'
        header = """
                    <para fontSize = 12>
                        Folio: <b>{0}</b> <br />
                        Sucursal: <b>{1}</b> <br />
                        Tipo:<b> {2}</b> <br />
                        Fecha: <b>{3}</b> <br />
                 """.format(eh.id, eh.branch.name, eh.action,eh.date_time.strftime('%d-%b-%Y'))
        if eh.printed:
            header += "<b> REIMPRESI&Oacute;N </b>"
        header += "</para>"
        footer = """
                    <para fontSize = 12>
                        Fecha de impresi&oacute;n: <b>{0}</b> <br />
                        Comentarios: <b>{1}</b> <br />
                        Balco Joyeros - Salida de Mercanc&iacute;a<br/>
                """.format(dt_now.strftime('%d-%b-%Y'), eh.extra)
        if eh.printed:
            footer += "<b> REIMPRESI&Oacute;N</b>"
        footer += "<para>"
        pdf = PDFReporter(response, 'Letter', header, footer)
        response = pdf.print_entries(eh, ehds)
        eh.printed = True
        eh.save()
        return response
    except:
        logger.debug("Error while retrieveing entries history \n{0}".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"error\", \"message\":\"\"}", content_type="application/json")



@login_required
def print_entries_report(request, id):
    logger.debug("Creating Report for: {0}".format(id))
    try:
        dt_now = datetime.utcnow().replace(tzinfo = pytz.utc)
        eh = ExistenceHistory.objects.get(id = id)
        ehds = ExistenceHistoryDetail.objects.filter(existence = eh).order_by('product__name')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename=Reporte_Entradas_' + eh.branch.name + '_' + eh.date_time.strftime('%d-%b-%Y') + '.pdf'
        header = """
                    <para fontSize = 12>
                        Folio: <b>{0}</b> <br />
                        Sucursal: <b>{1}</b> <br />
                        Tipo:<b> {2}</b> <br />
                        Fecha: <b>{3}</b> <br />
                 """.format(eh.id, eh.branch.name, eh.action,eh.date_time.strftime('%d-%b-%Y'))
        if eh.printed:
            header += "<b> REIMPRESI&Oacute;N </b>"
        header += "</para>"
        footer = """
                    <para fontSize = 12>
                        Fecha de impresi&oacute;n: <b>{0}</b> <br />
                        Comentarios: <b>{1}</b> <br />
                        Balco Joyeros - Entrada de Mercanc&iacute;a<br/>
                """.format(dt_now.strftime('%d-%b-%Y'), eh.extra)
        if eh.printed:
            footer += "<b> REIMPRESI&Oacute;N</b>"
        footer += "<para>"
        pdf = PDFReporter(response, 'Letter', header, footer)
        response = pdf.print_entries(eh, ehds)
        eh.printed = True
        eh.save()
        return response
    except:
        logger.debug("Error while retrieveing entries history \n{0}".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"error\", \"message\":\"\"}", content_type="application/json")


@login_required
def existence_history(request, id):
    logger.debug("History iD to retrieve: {0}".format(id))
    try:
        eh = ExistenceHistory.objects.get(id = id)
        ehds = ExistenceHistoryDetail.objects.filter(existence = eh)
        ret = [ehd.as_json() for ehd in ehds]
        return render_to_response('inventory/existence_history.html', { 'entries': json.dumps(ret), 'eh':eh.as_json()},context_instance=RequestContext(request))
    except:
        logger.debug("Error while retrieveing entries history \n{0}".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"error\", \"message\":\"\"}", content_type="application/json")

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
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json")
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
                return HttpResponse("{ \"status\": \"ok\", \"message\":\"OK\"}", content_type="application/json")
            logger.debug(inv_entry)
            inv_entry.quantity += qty
            inv_entry.date_time = datetime.now()
            inv_entry.save()
            return HttpResponse("{ \"status\": \"ok\", \"message\":\"OK\"}", content_type="application/json")
        except:
            logger.error("Unexpected error:{0} ".format(sys.exc_info()[0]))
            logger.error("Error data: {0}".format(post_json))
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json")


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
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json")
        try:
            inventory = Inventory.objects.get(id=inv)
            try:
                inv_entry = InventoryEntry.objects.get(inv=inventory, product = product)

            except InventoryEntry.DoesNotExist:
                logger.error("No entry found")
                return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json")
            logger.debug(inv_entry)
            if (inv_entry.quantity - qty) < 0:
                logger.error("Negative Quantity:{0} ".format(qty))
                return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json")
            else:
                inv_entry.quantity -= qty
                inv_entry.date_time = datetime.now()
                inv_entry.save()
                return HttpResponse("{ \"status\": \"ok\", \"message\":\"OK\"}", content_type="application/json")
        except:
            logger.error("Unexpected error:\n{0} ".format(traceback.format_exc()))
            logger.error("Error data: {0}".format(post_json))
            return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json")

@login_required
def update_entry(request):
    if not request.is_ajax():
        return HttpResponse(null, status=404)
    post_json = json.loads(request.POST['data'])
    eid = post_json['id']
    qty = post_json['qty']
    inv = request.session.get('inventory_id', False)
    if not inv:
        logger.error("No inventory found")
        return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json", status=404)
    try:
        inventory = Inventory.objects.get(id = inv)
        inv_entry = InventoryEntry.objects.get(inv = inventory, id = eid)
        inv_entry.quantity = qty
        inv_entry.save()
        return HttpResponse("{ \"status\": \"ok\", \"message\":\"OK\", \"id\":\"" + str(inv_entry.id) + "\", \"qty\":\"" + str(inv_entry.quantity) + "\"}", content_type="application/json")
    except:
        logger.error("Unexpected error:\n{0} ".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"error\", \"message\":\"No inventory\"}", content_type="application/json", status=500)


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

@login_required
def adjustments_inventory(request):
    try:
        inventory = Inventory.objects.get(enabled = True)
        branch = inventory.branch
        ies = inventory.inventoryentry_set.all().order_by('product__name')
        entries = []
        for ie in ies:
            tcount = ie.product.get_branch_transactions_count(branch)
            adjcnt = ie.get_adjustment_count()
            diff = tcount - ie.quantity - adjcnt
            entries.append({'entry': ie, 'tcount': tcount, 'diff': diff, 'adjcnt': adjcnt})
        exs = Existence.objects.filter(branch = branch)
        for ex in exs:
            ies = inventory.inventoryentry_set.filter(product = ex.product)
            if len(ies) > 0:
                continue
            sq = ex.product.get_branch_transactions_count(branch)
            if sq == 0:
                continue
            ie = InventoryEntry(inv = inventory,
                                product = ex.product,
                                quantity = 0,
                                user = request.user)
            ie.save()
            entries.append({'entry': ie, 'tcount': sq, 'diff': sq, 'adjcnt': 0})
        return render_to_response('inventory/adjustments_inventory.html', { 'entries': entries, 'inv_branch':inventory.branch.slug, 'inventory':inventory, 'enbale_form':True}, context_instance=RequestContext(request))
    except:
        logger.error("No inventory found")
        logger.error("Unexpected error:\n{0}".format(traceback.format_exc()))
        return render_to_response('inventory/adjustments_inventory.html', { 'entries': [] }, context_instance=RequestContext(request))
    #ret = [sale.as_json() for sale in sales]

@login_required
def get_adjustments(request, id):
    if not request.is_ajax():
        logger.debug("Request is not ajax")
        return HttpResponse("{ \"status\": \"404\", \"message\":\"No inventory\"}", content_type="application/json", status=404)
    try:
        inventory = Inventory.objects.get(enabled = True)
        ies = inventory.inventoryentry_set.filter(id = id)
        if len(ies):
            ie = ies[0]
        else:
            logger.debug("No products found")
            return HttpResponse("{ \"status\": \"500\", \"message\":\"No product found\"}", content_type="application/json", status=500)
        adjs = ie.inventoryadjustment_set.all()
        ret = [adj.as_json() for adj in adjs]
        return HttpResponse("{ \"status\": \"200\", \"message\":\"ok\", \"adjustments\": " + json.dumps(ret) + ", \"id\":\"" + id + "\"}", content_type="application/json")
    except:
        logger.error("Unexpected error:\n{0}".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"500\", \"message\":\"Error\"}", content_type="application/json", status=500)

@login_required
def save_adjustments(request):
    if not request.is_ajax():
        logger.debug("Request is not ajax")
        return HttpResponse("{ \"status\": \"404\", \"message\":\"No inventory\"}", content_type="application/json", status=404)
    try:
        inventory = Inventory.objects.get(enabled = True)
        post_json = json.loads(request.POST['data'])
        id = post_json['id']
        qty = post_json['qty']
        msg = post_json['msg']
        ies = inventory.inventoryentry_set.filter(id = id)
        if len(ies):
            ie = ies[0]
        else:
            logger.debug("No products found")
            return HttpResponse("{ \"status\": \"404\", \"message\":\"No product found\"}", content_type="application/json", status = 404)
        adj = InventoryAdjustment(inventory_entry = ie, quantity = qty, message = msg)
        adj.save()
        adjs = ie.inventoryadjustment_set.all()
        ret = [adj.as_json() for adj in adjs]
        logger.debug("ret: {0}".format(ret))
        return HttpResponse("{ \"status\": \"200\", \"message\":\"ok\", \"adjustments\": " + json.dumps(ret) + ", \"id\":" + str(ie.id) + "}", content_type="application/json")
    except:
        logger.error("Unexpected error:\n{0}".format(traceback.format_exc()))
        return HttpResponse("{ \"status\": \"500\", \"message\":\"Error\"}", content_type="application/json", status=500)
        
@login_required
def print_inventory_existence(request, id=None):
    if not request.user.is_superuser:
        return HttpResponse("{ \"status\": \"403\", \"message\":\"Error\"}", content_type="application/json", status=403)
    try:
        if id is None:
            inventory = Inventory.objects.get(enabled = True)
        else:
            inventory = Inventory.objects.get(id = id)
        branch = inventory.branch
        ies = inventory.inventoryentry_set.all().order_by('product__name')
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'filename=Reporte_Existencias_inv_' + inventory.branch.name + '_' + inventory.date_time.strftime('%d-%b-%Y') + '.pdf'
        header = """
                    <para fontSize = 12>
                        Reporte inventario {0} al {1}
                    </para>
                """.format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y'))
        footer = """
                    <para fontSize = 12>
                        Reporte inventario {0} al {1}
                    </para>
                 """.format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y'))
        pdf = PDFReporter(response, 'Letter', header, footer)
        response = pdf.print_inventory_existence(ies, "Reporte de inventario {0} al {1}".format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y')))
        return response
    except:
        logger.error("No inventory found")
        logger.error("Unexpected error:\n{0}".format(traceback.format_exc()))
        return HttpResponse("Error", status=500)

@login_required
def print_inventory_surplus(request):
    if not request.user.is_superuser:
        return HttpResponse("{ \"status\": \"403\", \"message\":\"Error\"}", content_type="application/json", status=403)
    try:
        inventory = Inventory.objects.get(enabled = True)
        branch = inventory.branch
        ies = inventory.inventoryentry_set.all().order_by('product__name')
        entries = []
        for ie in ies:
            tcount = ie.product.get_branch_transactions_count(branch)
            adjcnt = ie.get_adjustment_count()
            diff = tcount - ie.quantity - adjcnt
            if diff < 0:
                entries.append({'entry': ie, 'tcount': tcount, 'diff': diff, 'adjcnt': adjcnt})
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'filename=Reporte_Posible_Sobrante_inv_' + inventory.branch.name.replace(' ', '_') + '_' + inventory.date_time.strftime('%d-%b-%Y') + '.pdf'
        header = """
                    <para fontSize = 12>
                        Reporte Posible Sobrante {0} al {1}
                    </para>
                """.format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y'))
        footer = """
                    <para fontSize = 12>
                        Reporte Posible Sobrante {0} al {1}
                    </para>
                 """.format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y'))
        pdf = PDFReporter(response, 'Letter', header, footer)
        response = pdf.print_inventory_surplus(entries, "Reporte Posible Sobrante {0} al {1}".format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y')))
        return response
    except:
        logger.error("No inventory found")
        logger.error("Unexpected error:\n{0}".format(traceback.format_exc()))
        return HttpResponse("Error", status=500)

@login_required
def print_inventory_missing(request):
    if not request.user.is_superuser:
        return HttpResponse("{ \"status\": \"403\", \"message\":\"Error\"}", content_type="application/json", status=403)
    try:
        inventory = Inventory.objects.get(enabled = True)
        branch = inventory.branch
        ies = inventory.inventoryentry_set.all().order_by('product__name')
        entries = []
        for ie in ies:
            tcount = ie.product.get_branch_transactions_count(branch)
            adjcnt = ie.get_adjustment_count()
            diff = tcount - ie.quantity - adjcnt
            if diff > 0:
                entries.append({'entry': ie, 'tcount': tcount, 'diff': diff, 'adjcnt': adjcnt})
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'filename=Reporte_Posible_Faltante_inv_' + inventory.branch.name.replace(' ', '_') + '_' + inventory.date_time.strftime('%d-%b-%Y') + '.pdf'
        header = """
                    <para fontSize = 12>
                        Reporte Posible Faltante {0} al {1}
                    </para>
                """.format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y'))
        footer = """
                    <para fontSize = 12>
                        Reporte Posible Faltante {0} al {1}
                    </para>
                 """.format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y'))
        pdf = PDFReporter(response, 'Letter', header, footer)
        response = pdf.print_inventory_missing(entries, "Reporte Posible Faltante {0} al {1}".format(inventory.branch.name, inventory.date_time.strftime('%d-%b-%Y')))
        return response
    except:
        logger.error("No inventory found")
        logger.error("Unexpected error:\n{0}".format(traceback.format_exc()))
        return HttpResponse("Error", status=500)

@login_required
def transfers(request, branch = None):
    if branch is None:
        return render_to_response('inventory/transfers.html', context_instance=RequestContext(request))
    if request.GET.get('create', False):
        show_form = True
    else:
        show_form = False
    branches = request.user.employee.get_branches_slugs()
    if branch not in branches:
        return HttpResponse("{}", status = 500);
    tz = timezone('America/Monterrey')
    b = Branch.objects.get(slug = branch)
    tfrom = ProductTransfer.objects.exclude(status = 'delivered').filter(branch_from = b).order_by('date_time')
    trans_from = [{
            'id': o.id,
            'branch_from': o.branch_from,
            'branch_to': o.branch_to,
            'date_time': tz.normalize(o.date_time.astimezone(tz))
            } for o in tfrom]
    tto = ProductTransfer.objects.exclude(status = 'delivered').filter(branch_to = b)
    trans_to = [{
            'id': o.id,
            'branch_from': o.branch_from,
            'branch_to': o.branch_to,
            'date_time': tz.normalize(o.date_time.astimezone(tz))
            } for o in tto]
    return render_to_response('inventory/transfers/index.html', { 'branch': b, 'trans_from': trans_from, 'trans_to': trans_to, 'show_form': show_form}, context_instance=RequestContext(request))

@login_required
def save_transfer(request):
    post_json = json.loads(request.POST['data'])
    logger.debug('data: {0}'.format(post_json))
    user = request.user
    logger.debug('from {0}'.format(post_json['branch_from']))
    logger.debug('to {0}'.format(post_json['branch_to']))
    b_from = Branch.objects.get(slug = post_json['branch_from'])
    b_to= Branch.objects.get(slug = post_json['branch_to'])
    products = post_json['products']
    if len(products) == 0:
        return HttpResponse('{"response": "error", "message":"Transfer is empty"}', content_type='application/json')
    pt = ProductTransfer(branch_from = b_from, branch_to = b_to, status = 'sent', user = user)
    pt.save()
    eh_from = ExistenceHistory(branch = b_from, user = user, action = 'baja_tras', details="Traspaso")
    eh_from.save()
    for product in products:
        try:
            p = Product.objects.get(slug = product['code'])
            ptd = ProductTransferDetail(product = p, quantity = product['qty'], product_transfer = pt)
            ptd.save()
            ehd = ExistenceHistoryDetail(product = p, quantity = product['qty'], existence = eh_from)
            ehd.save()

        except:
            logger.error("Unexpected error in Transfer:\n{0}".format(traceback.format_exc()))
    return HttpResponse("{ \"status\": \"ok\", \"message\":\"ok\"}", content_type="application/json")

def accept_transfer(request, id):
    pt = ProductTransfer.objects.get(id = id)
    branch = pt.branch_to.slug
    branches = request.user.employee.get_branches_slugs()
    if branch not in branches:
        return HttpResponse("{}", status = 500);

    ptds = pt.producttransferdetail_set.all()
    eh_to = ExistenceHistory(branch = pt.branch_to, user = request.user, action = 'alta_tras', details = "Traspaso")
    eh_to.save()
    logger.debug("eh id: {0}".format(eh_to.id))
    for ptd in ptds:
        try:
            ehd = ExistenceHistoryDetail(product = ptd.product, quantity = ptd.quantity, existence = eh_to)
            ehd.save()
            logger.debug("ehd id: {0}".format(ehd.id))
        except:
            logger.error("Unexpected error in Transfer:\n{0}".format(traceback.format_exc()))
    pth = ProductTransferHistory(status_previous = pt.status, status_changed = 'delivered', product_transfer = pt, user = request.user)
    pth.save()
    pt.status = 'delivered'
    pt.save()
    return redirect('products-transfers')
