from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^create_account/$', views.create_account, name='create_account'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login_user/$', views.login_user, name='login_user'),
	url(r'^member_home$', views.member_home, name='member_home'),
	url(r'^add_recipe$', views.add_recipe, name='add_recipe'),
	url(r'^logout_user$', views.logout_user, name='logout_user'),
	url(r'^member/recipe(\d+)/$', views.member_recipe, name='member_recipe'),
	url(r'^remove_recipe$', views.remove_recipe, name='remove_recipe'),
	url(r'^add_note$', views.add_note, name='add_note'),
	url(r'^remove_note$', views.remove_note, name='remove_note'),
	url(r'^authenticate_user$', views.authenticate_user, name='authenticate_user'),


]

