from django.shortcuts import render
from django.http import JsonResponse
import requests

# Create your views here.
def org_members(request):
	user = request.user
	social_account = user.socialaccount_set.get(user=user.id)
	application_token = social_account.socialtoken_set.get(account=social_account.id)
	token = application_token.token

	url = "https://api.github.com/orgs/joinCODED/members"
	response = requests.get(url, headers={'Authorization': 'token '+token})
	#return JsonResponse(response.json(), safe=False)

	return render(request, "org_members.html", {'response':response.json()})


def repos(request):
	user = request.user
	social_account = user.socialaccount_set.get(user=user.id)
	application_token = social_account.socialtoken_set.get(account=social_account.id)
	token = application_token.token

	url = "https://api.github.com/user/repos"
	response = requests.get(url, headers={'Authorization': 'token '+token})
	#return JsonResponse(response.json(), safe=False)

	return render(request, "repos.html", {'repos':response.json()})

