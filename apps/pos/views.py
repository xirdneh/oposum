from django.shortcuts import render, render_to_response
from oPOSum.apps.branches.decorators import needs_branch
from django.template import RequestContext
from django.http import HttpResponse
from oPOSum.apps.products.models import Product, Provider
from oPOSum.apps.branches.models import Branch
from oPOSum.apps.pos.models import POSFolio, Sale, SaleDetails
from django.contrib.auth.models import User
from datetime import datetime
import logging
import json
from decimal import Decimal

# Create your views here.
logger = logging.getLogger("oPOSum.pos")

def get_pos_folio(branch, type):
    b = branch
    f = POSFolio.objects.select_for_update().get(branch = b, name=type)
    f_val = f.value
    f.value = f_val + 1
    f.save()
    return f_val

def sales(request):
    return render_to_response('pos/sales.html', context_instance=RequestContext(request))

def save_sale(request):
    if request.is_ajax():
        post_json = json.loads(request.POST['data'])
        user = User.objects.get(username=post_json['user'])
        b_slug = post_json['branch']
        branch = Branch.objects.get(pk = post_json['branch'])
        details = post_json['details']
        folio = get_pos_folio(branch,'ventas')
        pt = post_json['payment_type']
        pa = Decimal(post_json['payment_amount'])
        prods = []
        total = Decimal("0.0")
        for detail in details:
            total += Decimal(detail['qty']) * Decimal(detail['price'])
            try:
                p = Product.objects.get(slug = detail['slug'])
                sd = SaleDetails(product = p, quantity = int(detail['qty']), over_price = Decimal(detail['price']))
                sd.save()
                prods.append(sd)
            except Product.DoesNotExist:
                pr = Provider.objects.get(sku = "00")
                p = Product(slug = detail['slug'], regular_price = Decimal(detail['price']), provider=pr)
                p.save()
                sd = SaleDetails(product = p, quantity = int(detail['qty']), over_price = Decimal(detail['price']))
                sd.save()
                prods.append(sd)
        s = Sale(branch = branch, user = user, total_amount = total, folio_number = folio, payment_method = pt, payment_amount = pa)
        s.save()
        for sd in prods:
            sd.sale = s
            sd.save()
 
    return HttpResponse("{\"reponse\": \"OK\", \"folio\":\"" + str(folio)+ "\", \"ticket_pre\":\"" + branch.ticket_pre.encode('unicode_escape')+ "\", \"ticket_post\":\"" + branch.ticket_post.encode('unicode_escape') + "\"}", mimetype="application/json")

def get_sales_report(request, branch, urldatetime):
    date_time = urldatetime.split('-')
    start_date = datetime(int(date_time[2]), int(date_time[1]), int(date_time[0]), 0, 0)
    end_date = datetime(int(date_time[2]), int(date_time[1]), int(date_time[0]), 23, 59)
    sales = Sale.objects.filter(branch__slug = branch).filter(date_time__range=(start_date, end_date)).order_by('date_time')
    ret = [sale.as_json() for sale in sales]
    return HttpResponse("{\"response\": \"OK\", \"sales\":" + json.dumps(ret) + "}", mimetype="application/json")
