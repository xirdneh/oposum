from django.shortcuts import render, render_to_response
from oPOSum.apps.branches.decorators import needs_branch
from django.template import RequestContext
from django.http import HttpResponse
from oPOSum.apps.products.models import Product, Provider
from oPOSum.apps.branches.models import Branch
from oPOSum.apps.pos.models import POSFolio, Sale, SaleDetails
from oPOSum.apps.inventory.models import Existence
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
import logging, traceback
import json
from decimal import Decimal

# Create your views here.
def index(request):
    return render_to_response('/pos/layaway/index.html', context_instance=RequestContext(request))
