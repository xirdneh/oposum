from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
# Create your views here.

@login_required
def entries(request):
    pass

@login_required
def add_existence(request):
    return render_to_response('inventory/add_existence.html', 
                              context_instance=RequestContext(request))
