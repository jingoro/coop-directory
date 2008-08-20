from django.conf.urls.defaults import *

urlpatterns = patterns('coopdirectory.coops.views',
    (r'^(\d+)$', 'coop_detail'),
    (r'^$', 'coop_list'),
)

