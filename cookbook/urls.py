from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^recipe(\d+)/$', views.single_recipe, name='single_recipe')
]

