from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from oPOSum.apps.authentication.models import Employee
from oPOSum.apps.branches.models import Branch
from django.core import serializers

def login_user(request):
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                branches = user.employee.branch.all()
                request.session['user_branches'] = serializers.serialize("json", branches)
                request.session['all_branches'] = serializers.serialize("json", Branch.objects.all())
                request.session['oficina_branch'] = serializers.serialize("json", Branch.objects.filter(slug="oficina"))
                if 'branch_selected' not in request.session:
                    if len(branches) > 1:
                        request.session['branch_selected'] = 'None'
                    else:
                        request.session['branch_selected'] = branches[0].pk
                if [branch for branch in branches if branch.name.lower() == 'oficina']:
                    request.session['oficina'] = True
                return render(request, 'index.html')
            else:
                return render(request, 'index.html', { 'message':u'usuario/contrasena no existente'})
        else:
            return render(request, 'index.html', { 'message':u'usuario/contrasena no existente'})
    else:
        return render(request, 'index.html', { 'message':u'Favor de ingresar usuario/contrasena'})


def logout_user(request):
    logout(request)
    return render(request, 'index.html', { 'message':u'Usted ha cerrado sesion correctamente.'}) 
