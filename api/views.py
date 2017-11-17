from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import QueryForm
from TwitterSearch import *
import pyrebase
import os
import tmdbsimple as tmdb

def initializationDb():
	config = {
		"apiKey": os.environ['apiKey'],
		"authDomain": os.environ['authDomain'],
		"databaseURL": os.environ['databaseURL'],
		"storageBucket": os.environ['storageBucket']
	}
	firebase = pyrebase.initialize_app(config)
	email = os.environ['email']
	password = os.environ['password']
	# Get a reference to the auth service
	auth = firebase.auth()

	# Log the user in
	user = auth.sign_in_with_email_and_password(email, password)

	# Get a reference to the database service
	return firebase.database(), user['idToken']
	
@require_http_methods(["GET"])
def search(request):
	db, token = initializationDb()
	result = db.child("tweet").get(token)
	return JsonResponse(result.val())

@require_http_methods(["GET","POST"])
def save(request):
	if request.method == 'GET':
		form = QueryForm()
		return render(request, 'save.html', {'form': form})
	elif request.method == 'POST':
		form = QueryForm(request.POST)
		if form.is_valid():
			try:
				db, token = initializationDb()
				lang = request.POST.get("lang", "en")
				queryRaw = request.POST.get("query", "Film")
				query = queryRaw.split()
				tso = TwitterSearchOrder()
				tso.set_keywords(query)
				tso.set_include_entities(False)
				if lang == 'en' or lang == 'id':
					tso.set_language(lang)
						
				ts = TwitterSearch(
					consumer_key = os.environ['consumerKey'],
					consumer_secret = os.environ['consumerSecret'],
					access_token = os.environ['accessToken'],
					access_token_secret = os.environ['accessTokenSecret']
				)
						
				for tweet in ts.search_tweets_iterable(tso):
					# Pass the user's idToken to the push method
					data = {"username": tweet['user']['screen_name'], "tweet":tweet['text'],
					"favorite_count": tweet['favorite_count'], "retweet_count": tweet['retweet_count'], "lang":lang}
					db.child("tweet").child(tweet['id']).set(data, token)
				return HttpResponse("Success")
			except TwitterSearchException as e:
				return HttpResponse(e)
		else:
			return HttpResponse("Not Valid")
	
@require_http_methods(["GET","POST"])
def movie_list(request):
	tmdb.API_KEY = os.environ['KEY-MDB']
	discover = tmdb.Discover()
	movies = discover.movie(year=2017, sort_by=release_date.desc, release_date_gte='2017-11-01', release_date_lte='2017-11-30', page=5)
	return HttpResponse(movies)
