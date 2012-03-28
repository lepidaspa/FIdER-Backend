from django.conf.urls.defaults import url, patterns, include
from rest_api import v1_api


urlpatterns = patterns('',
    url(r'^/', include(v1_api.urls)),
)
