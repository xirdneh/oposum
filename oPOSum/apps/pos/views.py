from django.shortcuts import render
from oPOSum.apps.branches.decorators import needs_branch
from django.template import RequestContext
from django.http import HttpResponse
from oPOSum.apps.products.models import Product, Provider
from oPOSum.apps.branches.models import Branch
from oPOSum.apps.pos.models import POSFolio, Sale, SaleDetails
from oPOSum.apps.inventory.models import Existence
from oPOSum.libs import utils as pos_utils
from oPOSum.libs import sales as sales_utils
from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from django.conf import settings
import pytz
import logging, traceback
import json
from decimal import Decimal

# Create your views here.
logger = logging.getLogger(__name__)
log_sales = logging.getLogger("sales")

def get_pos_folio(branch, type):
    with transaction.atomic():
        b = branch
        f = POSFolio.objects.select_for_update().get(branch = b, name=type)
        f_val = f.value
        f.value = f_val + 1
        f.save()
    return f_val

def sales(request):
    return render(request, 'pos/sales.html')

def mock_sales(request):
    return render(request, 'pos/mocok_sales.html')

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
        allowed_data = open("{0}/../libs/branches.json".format(settings.PROJECT_DIR))
        allowed = json.load(allowed_data)
        if len(details) == 0:
            return HttpResponse("{\"response\": \"error\", \"message\":\"Sale is empty\"}", content_type="application/json", status = 500)
        else: 
            s = Sale(branch = branch, user = user, total_amount = 0, folio_number = folio, payment_method = pt, payment_amount = pa)
            s.save()
        for detail in details:
            total += Decimal(detail['qty']) * Decimal(detail['price'])
            try:
                p = Product.objects.get(slug = detail['slug'])
                sd = SaleDetails(product = p, quantity = int(detail['qty']), over_price = Decimal(detail['price']), sale = s)
                sd.save()
            except Product.DoesNotExist:
                pr = Provider.objects.get(sku = "00")
                p = Product(name = detail['slug'], slug = detail['slug'].replace('-', ''), regular_price = Decimal(detail['price']), provider=pr)
                p.save()
                sd = SaleDetails(product = p, quantity = int(detail['qty']), over_price = Decimal(detail['price']), sale = s)
                sd.save()
                prods.append(sd)
            try:
                branch = Branch.objects.get(pk = post_json['branch'])
                if branch.slug in allowed['allowed']:
                    pe = Existence.objects.get(product__slug = detail['slug'], branch = branch)
                    pe.quantity -= int(detail['qty'])
                    pe.save()
            except:
                log_sales.error("Error while substracting existance branch {0} - {1}:\n{2}\n".format(branch, detail['slug'], traceback.format_exc())) 
        #s = Sale(branch = branch, user = user, total_amount = total, folio_number = folio, payment_method = pt, payment_amount = pa)
        #s.save()
        #for sd in prods:
        #    sd.sale = s
        #    sd.save()
        s.total_amount = total
        s.save()
        d = {
            'response': 'OK',
            'folio': str(folio),
            'ticket_pre': branch.ticket_pre.encode('unicode_escape'),
            'ticket_post': branch.ticket_post.encode('unicode_escape'),
            'sale': s.as_json(),
            'ticket_str': sales_utils.ticket_text(s, folio).encode('unicode_escape')
        }
        log_sales.debug("Sale folio: %s, ip: %s", folio, 
                    request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR', ''))
    return HttpResponse(json.dumps(d, encoding='latin-1'), content_type="application/json")

def mock_sale(request):
    post_json = json.loads(request.POST['data'])
    user = User.objects.get(username=post_json['user'])
    branch = Branch.objects.get(pk = post_json['branch'])
    details = post_json['details']
    folio = get_pos_folio(branch,'ventas_mock')
    pt = post_json['payment_type']
    pa = Decimal(post_json['payment_amount'])
    prods = []
    total = Decimal("0.0")
    if len(details) == 0:
        return HttpResponse(
            "{\"response\": \"error\", \"message\":\"Sale is empty\"}",
            content_type="application/json",
            status = 500
        )
    else: 
        s = {
            "branch": {"slug": branch.slug, "name": branch.name},
            "user": user.username,
            "date_time": datetime.now().strftime(
                "%d/%m/%Y"
            ),
            "total_amount": Decimal(0),
            "payment_method": pt,
            "payment_amount": pa,
            "folio_number": str(folio),
            "ticket_pre": branch.ticket_pre.encode("unicode_escape"),
            "ticket_post": branch.ticket_post.encode("unicode_escape"),
            "sale_details": []
        }
    for detail in details:
        total += Decimal(detail['qty']) * Decimal(detail['price'])
        s["sale_details"].append({
            "product": {
                "name": detail["slug"],
                "slug": detail["slug"].replace("-", ""),
                "provider": "Provider",
                "categories": [],
                "regular_price": detail["price"],
                "equivalency": "1.00",
                "description": "Producto varios."
            },
            "quantity": str(detail["qty"]),
            "over_price": str(detail["price"])
        })
        try:
            p = Product.objects.get(slug = detail['slug'])
            s["sale_details"][-1]["product"]["description"] = p.description
            s["sale_details"][-1]["product"]["categories"] = [
                {"name": c.name,
                "slug": c.slug,
                "type": c.type } for c in p.category.all()
            ]
        except Product.DoesNotExist:
            pass
    s["total_amount"] = total
    d = {
        'response': 'OK',
        'folio': str(folio),
        'ticket_pre': branch.ticket_pre.encode('unicode_escape'),
        'ticket_post': branch.ticket_post.encode('unicode_escape'),
        'sale': s,
        'ticket_str': sales_utils.mock_ticket_text(
            s,
            folio
        ).encode('unicode_escape')
    }
    s["payment_amount"] = str(s["payment_amount"])
    s["total_amount"] = str(total)
    return HttpResponse(json.dumps(d, encoding='latin-1'), content_type="application/json")

def get_sales_report(request, branch, urldatetime):
    tz = pytz.timezone('America/Monterrey')
    utz = pytz.timezone('UTC')
    if urldatetime is None or urldatetime == '':
        utc = datetime.utcnow()
        utc = utc.replace(tzinfo=utz) 
        now = utc.astimezone(tz)
        date_time = now.strftime("%d-%m-%Y")
        date_time = date_time.split('-')

    else:
        date_time = urldatetime.split('-')
    ret = {}
    start_date = datetime(int(date_time[2]), int(date_time[1]), int(date_time[0]), 0, 0)
    start_date = tz.localize(start_date)
    start_date = pytz.utc.normalize(start_date.astimezone(tz))
    end_date = datetime(int(date_time[2]), int(date_time[1]), int(date_time[0]), 23, 59)
    end_date = tz.localize(end_date)
    end_date = pytz.utc.normalize(end_date.astimezone(tz))
    sales = Sale.objects.get_sales_json(branch, start_date, end_date)
    ret['sales'] = sales
    apps = pos_utils.get_installed_oposum_apps()
    if 'layaway' in apps:
        from oPOSum.apps.layaway.models import LayawayHistory
        payments = LayawayHistory.objects.get_payments_json(branch, start_date, end_date)
        ret['payments'] = payments
    return HttpResponse("{\"response\": \"OK\", \"data\":" + json.dumps(ret, encoding="latin-1") + "}", content_type="application/json")

def get_sales_report_branch(request, branch, datestart, dateend=None):
    tz = pytz.timezone('America/Monterrey')
    if(dateend is None):
        dt = datetime.utcnow()
        end_date = datetime(dt.year, dt.month, dt.day, 23, 59)
    else:
        dt = dateend.split('-')
        end_date = datetime(int(dt[2]), int(dt[1]), int(dt[0]), 23, 59)
    end_date = tz.localize(end_date)
    end_date = pytz.utc.normalize(end_date.astimezone(tz))
    dt = datestart.split('-')
    start_date = datetime(int(dt[2]), int(dt[1]), int(dt[0]), 0, 0)
    start_date = tz.localize(start_date)
    start_date = pytz.utc.normalize(start_date.astimezone(tz))
    ret = Sale.objects.get_sales_structure(branch, start_date, end_date)
    b = Branch.objects.get(slug = branch) 
    return render(request, 'pos/sale_details_report.html', 
                                { 'sales':ret['sales'], 
                                  'totales':ret['totales'], 
                                  'folio_start': ret['folio_start'], 
                                  'folio_end': ret['folio_end'], 
                                  'datestart': start_date.strftime("%d-%B-%Y"), 
                                  'dateend':end_date.strftime("%d-%B-%Y"), 
                                  'branch': b.name })
