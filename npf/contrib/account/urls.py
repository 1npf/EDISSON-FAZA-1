from django.conf.urls import patterns, url

from npf.contrib.account.views import *


urlpatterns = patterns('',
    url(r'process_account/$', ProcessAccount.as_view()),

)