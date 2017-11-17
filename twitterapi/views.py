from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
import os

def index(request):
	return HttpResponse('Welcome to Twitter Crawler API.')
