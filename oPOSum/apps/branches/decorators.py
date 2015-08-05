from functools import wraps
from django.shortcuts import redirect, resolve_url
from django.http import HttpResponseRedirect


def needs_branch(function, redirect_url="/branches/select_branch/"):
    @wraps(function)
    def inner(request, *args, **kwargs):
        if request.session['branch_selected'] == 'None':
            redirect(resolve_url(redirect_url))
        else:
            function(request, *args, **kwargs)
    return inner
