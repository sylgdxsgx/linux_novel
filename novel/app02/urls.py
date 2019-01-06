from django.conf.urls import url
# from django.conf.urls import patterns
from app02 import views

urlpatterns = [
    #url(r'^accounts/login/$','django.contrib.auth.views.login'),
    url(r'^$',views.login,name='login'),
    url(r'^login$',views.login,name='login'),
    url(r'^logout$',views.logout),
    url(r'^index$',views.index),
    url(r'^regist$',views.regist),
    url(r'^reset_password$',views.reset_password),
    url(r'^machine$',views.machine),
    url(r'^monitor$',views.monitor),
    url(r'^addproject$',views.addproject),
    url(r'^addpoint$',views.addpoint),
    url(r'^addmachine$',views.addmachine),
    #url(r'',views.tologin),
]
