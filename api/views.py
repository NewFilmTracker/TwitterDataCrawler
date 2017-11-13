from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from TwitterSearch import *
import pyrebase
import os

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
	return firebase.database()
	
@require_http_methods(["GET"])
def search(request):
	db = initializationDb()
	result = db.child("tweet").get(user['idToken'])
	return JsonResponse(result.val())

@require_http_methods(["POST"])
def save(request):
	db = initializationDb()
	
	try:
		lang = request.POST.get("lang", "en")
		queryRaw = request.POST.get("query", "Film")
		tso = TwitterSearchOrder()
		query = queryRaw.split()
		tso.set_keywords(query)
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
			db.child("tweet").child(tweet['id']).set(tweet, user['idToken'])
		return JsonResponse({'status':200, 'message':'Success Saved to Database'})
	except TwitterSearchException as e:
		return HttpResponse(e)
