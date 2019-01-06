from django.conf.urls import url
# from django.conf.urls import patterns
from shufa import views

urlpatterns = [
	url(r'^$',views.index),
    url(r'^index$',views.index),
	url(r'^raky.asp', views.raky),
	url(r'^database',views.database),
]