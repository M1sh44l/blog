from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from .models import Like
from django.shortcuts import get_object_or_404
from .forms import PostForm, UserSignUp, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def usersignup(request):
	context = {}
	form = UserSignUp()
	context['form'] = form
	if request.method == "POST":
		form = UserSignUp(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = user.username
			password = user.password
			user.set_password(password)
			user.save()
			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)

			return redirect("posts:list")
		messages.error(request, form.errors)
		return redirect("posts:signup")
	return render(request, 'signup.html', context)

def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form
	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect("posts:list")
			messages.warning(request, "Wrong username/password combination. Please try again.")
			return redirect("posts:login")
		messages.warning(request, form.errors)
		return redirect("posts:login")
	return render(request, "login.html", context)

def userlogout(request):
	logout(request)
	return redirect("posts:login")

def post_list(request):
	today = timezone.now().date()
	#obj_list = Post.objects.all()
	if request.user.is_superuser or request.user.is_staff:
		obj_list = Post.objects.all()
	else:
		obj_list = Post.objects.filter(draft=False).filter(publish__lte=today)

	# Here activating the search bar which was done in the post_list.html i.e. "q"
	query = request.GET.get("q")
	if query:
		obj_list = obj_list.filter(
			Q(title__icontains=query)|
			Q(content__contains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()

	#Listing through pages whenever necessary
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
		"today": today,
		"query": query,
	}
	return render(request, "post_list.html", context)

def post_detail(request, slug):
	obj = get_object_or_404(Post, slug=slug)
	date = timezone.now().date()

	if obj.publish > date or obj.draft:
		if not(request.user.is_superuser or request.user.is_staff):
			raise Http404

	if request.user.is_authenticated():
		if Like.objects.filter(postLike=obj, user=request.user).exists():
			liked = True
		else:
			liked = False

	post_like_count = obj.like_set.all().count()

	context = {
			"instance": obj,
			"liked": liked,
			"like_count": post_like_count,
	}
	return render(request, "post_detail.html", context)

def like_count(request, post_id):
	post_object = Post.objects.get(id=post_id)

	like, created = Like.objects.get_or_create(user=request.user, postLike=post_object)

	if created:
		action="like"
	else:
		action="unlike"
		like.delete()

	post_like_count = post_object.like_set.all().count()
	response = {
		"action": action,
		"like_count": post_like_count,

	}

	return JsonResponse(response, safe=False)

def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.author = request.user
		obj.save()
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

