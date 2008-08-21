from django.conf.urls.defaults import *

urlpatterns = patterns('coops.views',
    (r'^(\d+)$', 'coop_detail'),
    (r'^add$', 'coop_add'),
    (r'^$', 'coop_list'),
)
