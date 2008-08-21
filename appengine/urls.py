from django.conf.urls.defaults import *

import settings

urlpatterns = patterns('',
    (r'^coops/', include('coops.urls')),
    #TODO: Change this to a better front page.
    (r'^$', 'coops.views.coop_list'),
)

# Serve static files and show indeces if we are in debug mode.
if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^dev_media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT,
                    'show_indexes': True}),
    )
