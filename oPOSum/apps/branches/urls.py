from django.conf.urls import include, url
from oPOSum.apps.branches import views as branches_views

urlpatterns = [
    url(r'^select_branch/?', branches_views.select_branch, name="branches-select_branch"),
]
