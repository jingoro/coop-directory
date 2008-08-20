from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from coopdirectory import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^coops/', include('coopdirectory.coops.urls')),
    #TODO: Change this to a better front page.
    (r'^$', 'coopdirectory.coops.views.coop_list'),
)

# Serve static files and show indeces if we are in debug mode.
if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^dev_media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT,
                    'show_indexes': True}),
    )
