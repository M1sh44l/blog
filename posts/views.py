from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.
def post_create(request):
	post_list = Post.objects.all()
	post_filter = Post.objects.filter(content__icontains="python").first()
	context = {
		"title": "Post Page",
		"content": "This is just a simple paragraph",
		"user": request.user,
		"list": post_list,
		"filter": post_filter,
	}
	return render(request, "create.html", context)

def post_update(request):
	return render(request, "update.html", {})

def post_delete(request):
	return render(request, "delete.html", {})

def post_list(request):
	return HttpResponse("<h1> list </h1>")

def post_detail(request):
	return HttpResponse("<h1> Detail </h1>")

def post_content(request):
	return HttpResponse("<h2> Content </h2>")

def post_image(request):
	return HttpResponse("<h2> Image </h2>")

def post_contact(request):
	return HttpResponse("<h2> Contact </h2>")
