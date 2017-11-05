from django.shortcuts import render
from django.http import HttpResponse
from TwitterSearch import *
import pyrebase
import os
import json

def search(request):
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
	db = firebase.database()
	
	try:
		tso = TwitterSearchOrder()
		tso.set_keywords(['Film', 'Batman'])
		tso.set_language('en')
		
		ts = TwitterSearch(
			consumer_key = os.environ['consumerKey'],
			consumer_secret = os.environ['consumerSecret'],
			access_token = os.environ['accessToken'],
			access_token_secret = os.environ['accessTokenSecret']
		)
		
		for tweet in ts.search_tweets_iterable(tso):
			# Pass the user's idToken to the push method
			db.child("tweet").child(tweet['id']).set(tweet)
		result = db.child("tweet").get()
		return JsonResponse(result.val())

	except TwitterSearchException as e:
		return HttpResponse(e)
