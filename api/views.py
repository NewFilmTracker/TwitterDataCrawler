from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
# Create your views here.
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

	# data to save
	data = {
		"name": "Mortimer 'Morty' Smith"
	}

	# Pass the user's idToken to the push method
	results = db.child("users").push(data, user['idToken'])
	return HttpResponse(data)
