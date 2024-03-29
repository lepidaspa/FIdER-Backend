from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import meta_model
import storage

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LabsBackend.views.home', name='home'),
    # url(r'^LabsBackend/', include('LabsBackend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^meta/', include(meta_model.urls)),
    url(r'^backend/', include(storage.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
