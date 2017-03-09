from django.conf.urls import url
from board import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name>[\w]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name>[\w]+)/add_post/$', views.add_post, name='add_post'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

]

