from django.conf.urls.defaults import url, patterns, include
from api import *

urlpatterns = patterns('',
    url(r'^/', include(Constructor.urls)),
)
