from django.shortcuts import render
from oPOSum.apps.branches.decorators import needs_branch
from django.template import RequestContext
from django.http import HttpResponse
from oPOSum.apps.products.models import Product, Provider
from oPOSum.apps.branches.models import Branch
from oPOSum.apps.inventory.models import Existence
from oPOSum.apps.client.models import Client
from oPOSum.apps.layaway.models import Layaway, LayawayHistory, LayawayProduct
from oPOSum.libs import utils as pos_utils
from oPOSum.libs import layaway as layaway_utils
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import F
from datetime import datetime
from django.conf import settings
import logging, traceback
import json
from decimal import Decimal
logger = logging.getLogger(__name__)
# Create your views here.
@login_required
def index(request):
    return render(request, '/pos/layaway/index.html')

@login_required
def add_layaway(request):
    pass

@login_required
def save_layaway(request):
    error = False
    msg = []
    if request.is_ajax():
        json_data = json.loads(request.POST['data'])
        branch_slug = json_data['branch_slug']
        logger.debug("Branch: {0}".format(branch_slug))
        allowed_data = open("{0}/../libs/branches.json".format(settings.PROJECT_DIR))
        allowed = json.load(allowed_data)

        if pos_utils.is_employee_in_branch(request, branch_slug):
            logger.debug("We have permission in Branch")
            logger.debug(json_data)
            b = Branch.objects.get(slug = branch_slug)
            products = json_data['products']
            payment_type = json_data['payment_type']
            payment = json_data['payment']
            client_id = json_data['client_id']
            layaway_type = json_data.get('layaway_type', 'one_month')
            layaway_type = layaway_utils.get_layaway_type(layaway_type)
            logger.debug("LT: {0}".format(layaway_type))
            client = Client.objects.get(id = client_id)
            if Layaway.objects.can_add_more(client):
                layaway =  Layaway(branch = b,
                                  client = client,
                                  user = request.user,
                                  type = layaway_type)
                layaway.save()
                for product in products:
                    try:
                        p = Product.objects.get(slug = product['code'])
                        try:
                            lp = LayawayProduct.objects.get(prod = p, layaway = layaway)
                        except LayawayProduct.DoesNotExist:
                            lp = LayawayProduct(prod = p, layaway=layaway, price=Decimal(product['retail_price']))
                        lp.qty += int(product['qty'])
                        lp.save()
                        if b.slug in allowed['allowed']:
                            e = Existence.objects.get(branch = b, product = p)
                            e.quantity = F('quantity') - int(product['qty'])
                            e.save()

                    except:
                        msg.append("LayawayProductError")
                        logger.error("There was an error substracting product in Layaway {0}: {1}".format(b.name, layaway.id))
                        logger.error("{0}".format(traceback.format_exc()))
                layaway.update_amount_to_pay()
                logger.debug("Layaway : {0} : {1} - {2}".format(layaway.id, layaway.get_debt_amount(), layaway.get_date_end()))
                msg.append("LayawaySaveSuccess")
                if layaway.get_debt_amount() - Decimal(payment) >= Decimal(0.0):
                    lh = LayawayHistory(branch = b,
                                        user = request.user,
                                        amount = Decimal(payment),
                                        payment_type = payment_type,
                                        layaway = layaway)
                    lh.save()
                    msg.append("LayawayPaymentSuccess")
                else:
                    error = True
                    msg.append("LayawayPaymentError")
            else:
                error = True
                msg.append("LayawayUserDebtError")
        else:
            error = True
            msg.append("LayawayUserBranchAccessError")
        if error:
            return HttpResponse("{ \"status\": \"error\", \"message\": " + json.dumps(msg, encoding="latin-1") + "}", content_type = "application/json")
        else:
            return HttpResponse("""{{ \"status\": \"ok\", 
                                     \"message\": {0},
                                     \"layaway\": {1},
                                     \"payment\": {2},
                                     \"branch\" : {3}
                                }}""".format(json.dumps(msg), 
                                             json.dumps(layaway.as_json(), encoding="latin-1"),
                                             json.dumps(lh.as_json()),
                                             json.dumps(layaway.branch.as_json())), content_type = "application/json")
    return render(request, '/layaway/index.html')

def save_payment(request):
    error = False
    msg = []
    if request.is_ajax():
        json_data = json.loads(request.POST['data'])
        branch_slug = json_data['branch_slug']
        if pos_utils.is_employee_in_branch(request, branch_slug):
            b = Branch.objects.get(slug = branch_slug)
            payment_type = json_data['payment_type']
            payment = json_data['payment']
            client_id = json_data['client_id']
            layaway_id = int(json_data['lid'])
            layaway = Layaway.objects.get(id = layaway_id)
            if layaway.get_debt_amount() - Decimal(payment) >= Decimal(0.0):
                lh = LayawayHistory(branch = b,
                                    user = request.user,
                                    amount = Decimal(payment),
                                    payment_type = payment_type,
                                    layaway = layaway)
                lh.save()
                msg.append("LayawayPaymentSuccess")
            else:
                error = True
                msg.append("LayawayPaymentError")
        else:
            error = True
            msg.append("LayawayUserBranchAccessError")
        if error:
            return HttpResponse("{ \"status\": \"error\", \"message\": " + json.dumps(msg) + "}", content_type = "application/json")
        else:
            return HttpResponse("""{{ \"status\": \"ok\", 
                                     \"message\": {0},
                                     \"layaway\": {1},
                                     \"payment\": {2},
                                     \"branch\" : {3}
                                }}""".format(json.dumps(msg), 
                                             json.dumps(layaway.as_json(), encoding="latin-1"),
                                             json.dumps(lh.as_json()),
                                             json.dumps(layaway.branch.as_json())), content_type = "application/json")
    return render(request, '/layaway/index.html')
