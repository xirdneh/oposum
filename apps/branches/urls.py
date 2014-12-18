from django.conf.urls import patterns, include, url

urlpatterns = patterns('oPOSum.apps.branches.views',
    url(r'^select_branch/?', 'select_branch', name="branches-select_branch"),
)
