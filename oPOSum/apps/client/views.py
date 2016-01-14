# -*- coding: utf-8
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from oPOSum.apps.client.forms import *
from oPOSum.apps.client.models import Client
from oPOSum.libs import utils as pos_utils
import logging, traceback
logger = logging.getLogger(__name__)

# Create your views here.

@login_required
def index(request):
    return render_to_response('clients/index.html', context_instance=RequestContext(request))

@login_required
def new(request, client_id = None):
    apps = pos_utils.get_installed_oposum_apps()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                c = form.save(commit=False)
                c.save()
                return render_to_response('clients/new.html', { 'form': form, 'client':c, 'apps':apps }, context_instance=RequestContext(request))
            except ValidationError as e:
                logger.error("Client Form Errors: {0}".format(e.message_dict))
        else:
            #logger.debug("Client debug {0}".format(form.errors['email']))
            logger.error("Client Form Errors: \n")
            for error in form.errors:
                logger.error("{0}".format(form.errors[error]))
            try:
                cc = Client.objects.get(phonenumber=request.POST['phonenumber'])
                return render_to_response('clients/new.html', { 'form': form, 'client':cc, 'apps':apps, 'message': 'Un cliente con la misma información ya existe. Abajo estan los datos de este cliente.' }, context_instance=RequestContext(request))
            except Client.DoesNotExist:
                logger.error("Client doesn't exists: \n")
    else:
        if not client_id is None:
            try:
                c = Client.objects.get(id=client_id)
                form = ClientForm(instance = c)
                ret = { 'form': form, 'client':c, 'apps':apps }
                if 'layaway' in apps:
                    from oPOSum.apps.layaway.models import Layaway
                    ls = [{'layaway': l, 'last_payment': l.get_last_payment(), 'payments': l.layawayhistory_set.all().order_by('date_time'), 'products': l.layawayproduct_set.all()}
                          for l in Layaway.objects.filter(client = c).order_by('-date_time')]
                    ret['layaways'] = ls
                if 'workshop' in apps:
                    from oPOSum.apps.workshop.models import WorkshopTicket
                    wts = [{'workshop_ticket': wt, 'last_payment': wt.get_last_payment(), 'payments': wt.workshoppayment_set.all().order_by('date_time')}
                            for wt in WorkshopTicket.objects.filter(client = c).order_by('date_time')]
                    ret['workshop_tickets'] = wts
                return render_to_response('clients/new.html',ret , context_instance=RequestContext(request))
            except Client.DoesNotExist:
                logger.debug("Search client id doesn't exist {0}".format(client_id))
        form = ClientForm()
    return render_to_response('clients/new.html', { 'form': form}, context_instance=RequestContext(request))

@login_required
def search(request):
    q = request.GET.get('q', '')
    if q:
        if '-' in q:
            q = q.replace('-', '')
        if ' ' in q:
            ql = q.split(' ')
            pnq = Q(phonenumber__contains=q[-1])
            idnq = Q(phonenumber__icontains=q[-1])
            fnq = Q(first_name__icontains=q[-1])
            lnq = Q(last_name__icontains=q[-1])
            eq = Q(email__icontains=q[-1])
            for i in ql[:-1]:
                pnq |= Q(phonenumber__contains=i)
                idnq |= Q(id_number__icontains=i)
                fnq |= Q(first_name__icontains=i)
                lnq |= Q(last_name__icontains=i)
                eq |= Q(email__icontains=q[-1])
            clients = Client.objects.filter(pnq | idnq | fnq | lnq | eq).order_by('first_name', 'last_name')
        else:
            clients = Client.objects.filter(
                Q(id_number__icontains = q) | 
                Q(phonenumber__contains = q) |
                Q(first_name__icontains = q) |
                Q(last_name__icontains = q) |
                Q(email__icontains = q)
                ).order_by('first_name', 'last_name')
        return render_to_response('clients/search.html',{'clients': clients}, context_instance=RequestContext(request))
    return render_to_response('clients/search.html',context_instance=RequestContext(request))
