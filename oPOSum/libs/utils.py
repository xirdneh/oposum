from django.conf import settings
import json

def get_installed_oposum_apps():
    apps = settings.INSTALLED_APPS
    ret_apps = []
    for app in apps:
        if 'oPOSum.apps' in app:
            ret_apps.append(app.split('.')[-1])
    return ret_apps

def is_branch_allowed(branch):
    allowed_data = open("{0}/../libs/branches.json".format(settings.PROJECT_DIR))
    allowed = json.load(allowed_data)
    if branch in allowed['allowed']:
        return True
    else:
        return False

def get_employee(request):
    if request.user.is_authenticated():
        return request.user.employee
    else:
        return False

def is_employee_in_branch(request, branch):
    if request.user.is_authenticated():
        e = request.user.employee
        b = e.get_branches_slugs()
        if branch in b:
            return True
    return False
