from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def entries(request):
    pass
