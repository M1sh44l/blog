from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404

# Create your views here.

def post_list(request):
    obj_list = Post.objects.all()#.order_by("-timestamp", "-updated")
    paginator = Paginator(obj_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)

    context = {
        "post_list": objs,
        "user": request.user.is_staff,
        "user2": request.user.is_superuser,
    }
    return render(request, "post_list.html", context)

def post_detail(request, slug):
	obj = get_object_or_404(Post, slug=slug)
	context = {
			"instance": obj,
			"share_string": quote(obj.content),
	}
	return render(request, "post_detail.html", context)

def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "OMG! Nice one!")
		return redirect("posts:list")
	context = {
		"form": form,
	}
	return render(request, "post_create.html", context)

def post_update(request, slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	post_object = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=post_object)
	if form.is_valid():
		form.save()
		messages.success(request, "Any second thought?")
		return redirect("posts:list")
	context = {
		"form": form,
		"post_object": post_object,
	}
	return render(request, "post_update.html", context)

def post_delete(request, slug):
	if not request.user.is_superuser:
		raise Http404
	delete_object = Post.objects.get(slug=slug)
	delete_object.delete()
	#or the above could be done in one line: delete_object = = Post.objects.get(id=post_id).delete()
	messages.warning(request, "Seriously bro?")
	return redirect("posts:list")

