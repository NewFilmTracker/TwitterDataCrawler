from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^search', views.search, name='search'),
	url(r'^savesearch', views.save, name='save'),
	url(r'^release', views.retrieve_movie, name='release'),
	url(r'^saverelease', views.movie_list, name='saverelease'),
	url(r'^popular', views.retrieve_popular, name='popular'),
	url(r'^savemovie', views.search_movie, name='savemovie'),
	url(r'^savepopular', views.popular_movie, name='savepopular'),
	url(r'^traindata', views.traindata, name='traindata')
]
