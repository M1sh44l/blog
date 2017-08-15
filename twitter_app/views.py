from django.shortcuts import render
from django.http import JsonResponse
from allauth.socialaccount.admin import SocialApp
from requests_oauthlib import OAuth1
from urllib.parse import quote
import requests


# Create your views here.
def twitterAPI(request):
	user = request.user
	twitter_account = user.socialaccount_set.get(user=user.id)
	application_token = twitter_account.socialtoken_set.get(account=twitter_account.id)
	token = application_token.token

	token_secret = application_token.token_secret

	social_application = SocialApp.objects.get(provider=twitter_account.provider)
	client_id = social_application.client_id
	client_secret = social_application.secret

	# the below code is required and in order-manner as per Twitter Authorization Requirements!
	required_auth = OAuth1(client_id, client_secret, token, token_secret)

	# using 'quote' here is to make it URL friendly since the '@' cannot be used/input!
	search_stuff = quote("from:m1shaal")

	url = "https://api.twitter.com/1.1/search/tweets.json?q=%s"%(search_stuff)
	response = requests.get(url, auth=required_auth)

	return JsonResponse(response.json(), safe=False)

	# return render(request, "org_members.html", {'response':response.json()})