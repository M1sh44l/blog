from django.shortcuts import render
from django.http import JsonResponse
import requests

# Create your views here.
def text_search(request):
	api_key = 'AIzaSyABfvAadceT8OHve6IosdhUTaeBQqJxRTs'
	query = request.GET.get("query", '')
	next_page_token = request.GET.get("next_page_token")
	url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s'%(query, api_key)
	#another way below to call for the Google API URL !
	#url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+query+'&key='+api_key

	if next_page_token is not None:
		url+="&pagetoken=%s"%(next_page_token)
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	context = {
	'response': response.json(),
	}
	return render(request, "text.html", context)


def place_detail(request):
	api_key = 'AIzaSyABfvAadceT8OHve6IosdhUTaeBQqJxRTs'
	key = 'AIzaSyDBYG0PgiSi5lEG-13nEAK-Q3GQz8pAqds'
	reference = request.GET.get("reference")
	url = 'https://maps.googleapis.com/maps/api/place/details/json?reference=%s&key=%s'%(reference, api_key)
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	context = {
	'response': response.json(),
	'key': key,
	}
	return render(request, "detail.html", context)

def nearby_search(request):
	api_key = 'AIzaSyBjoa7nxUN3NBBPW0y2vHKsmSxBelDEbBs'
	location = '-33.8670522,151.1957362'
	radius = 500
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&key=%s'%(location, radius, api_key)
	response = requests.get(url)
	context = {
	'response': response.json(),
	}
	# return JsonResponse(response.json(), safe=False)
	return render(request, "nearby.html", context)
