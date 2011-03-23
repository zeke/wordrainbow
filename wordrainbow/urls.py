from django.conf.urls.defaults import *
from wordnik import Wordnik

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


w = Wordnik(api_key="1d3baf57f57254b5c430200e729037e9dea9d87493f3a16b4")
urlpatterns = patterns('',
    (r'^(?P<mode>.*)/$', 'play.views.index', { "w": w } ),
    #(r'^mix$', 'play.mix.index', { "w": w } ),
    # Example:
    # (r'^wordrainbow/', include('wordrainbow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
