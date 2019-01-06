from django.conf.urls import url
# from django.conf.urls import patterns
from Intf import views
from Intf import views_if

urlpatterns = [
	url(r'^$',views.index),
    url(r'^index$',views.index),
    url(r'^login_action/$',views.login_action),
    url(r'^event_manage/$',views.event_manage),
    url(r'^guest_manage/$',views.guest_manage),
    url(r'^search_name/$',views.search_name),
    url(r'^sign_index/(?P<event_id>[0-9]+)/$',views.sign_index),
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$',views.sign_index_action),
    url(r'^logout/$',views.logout),
	url(r'^add_event/', views_if.add_event, name='add_event'),
	url(r'^add_guest/',views_if.add_guest,name='add_guest'),
	url(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
	url(r'^get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
	url(r'^user_sign/', views_if.user_sign, name='user_sign'),
]