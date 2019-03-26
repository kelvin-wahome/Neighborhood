from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Neighbourhood, Business, Profile, Join, Posts, Comments
import datetime as dt


@login_required(login_url='/accounts/login/')
def index(request):
    '''
    View function that renders the homepage
    '''
    neighbourhoods = Neighbourhood.objects.all()
    return render(request, 'index.html', locals())


@login_required(login_url='/accounts/login/')
def search_business(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        businesses = Business.objects.filter(
            name__icontains=search_term, hood=request.user.join.hood_id.id)
        searched_businesses = Business.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', locals())

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', locals())


@login_required(login_url='/accounts/login/')
def profile(request):
    '''
    View profile that renders a user's profile page
    '''
    profile = Profile.objects.get(user=request.user)

    return render(request, 'profile/profile.html', locals())


@login_required(login_url='/accounts/login/')
def update_profile(request):
    '''
    View function that enables a user to update their profile
    '''
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successful profile edit!')
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=profile)
        return render(request, 'profile/update_profile.html', locals())


@login_required(login_url='/accounts/login/')
def add_hood(request):
    '''
    View function that enables users to add hoods
    '''
    if request.method == 'POST':
        form = AddHoodForm(request.POST)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.user = request.user
            neighbourhood.save()
            messages.success(
                request, 'You Have succesfully created a hood.You may now join your neighbourhood')
            return redirect('home')

        else:
            form = AddHoodForm()
            return render(request, 'add_hood.html', locals())
@login_required(login_url='/accounts/login/')
def join_hood(request,hood_id):
	'''
	View function that enables users join a hood
	'''
	neighbourhood = Neighbourhood.objects.get(pk = hood_id)
	if Join.objects.filter(user_id = request.user).exists():

		Join.objects.filter(user_id = request.user).update(hood_id = neighbourhood)
	else:

		Join(user_id=request.user,hood_id = neighbourhood).save()

	messages.success(request, 'Success! You have succesfully joined this Neighbourhood ')
	return redirect('index')

def home(request):
  '''
  View function that renders users neighbourhood
  '''
  neighbourhoods = Neighbourhood.objects.filter(user=request.user)
  return render(request,'home.html',locals())

@login_required(login_url='/accounts/login/')
def edit_hood(request,hood_id):
	'''
	View function that enables a user to edit his/her neighbourhood details
	'''
	neighbourhood = Neighbourhood.objects.get(pk = hood_id)
	if request.method == 'POST':
		form = AddHoodForm(request.POST,instance = neighbourhood)
		if form.is_valid():
			form.save()
			messages.success(request, 'Neighbourhood edited successfully')

			return redirect('index')
	else:
		form = AddHoodForm(instance = neighbourhood)
		return render(request,'edit_hood.html',locals())
@login_required(login_url='/accounts/login/')
def leave_hood(request,id):
  '''
  Views that enables users leave a neighbourhood
  '''
  Join.objects.get(id = request.user.id).delete()
  return redirect('index')

@login_required(login_url='/accounts/login/')
def add_post(request):
  '''
  View function that enables a user to create a post in a neighbourhood
  '''
  if Join.objects.filter(user_id=request.user).exists():
    if request.method == 'POST':
      form = PostForm(request.POST)
      if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.hood = request.user.join.hood_id
        post.save()
        return redirect('index')

    else:
      form = PostForm()
      return render(request,'add_post.html',locals())
  else:
    messages.error(request,'Error!!Post can only be added after joining a neighbourhood!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def posts(request):
  '''
  View function that renders the posts page
  '''
  posts = Posts.objects.filter(user = request.user)
  return render(request,'posts.html',locals())

@login_required(login_url='/accounts/login')
def edit_post(request,post_id):
  '''
  View function that enables users edit their posts
  '''
  if Join.objects.filter(user_id=request.user).exists():
    post = Posts.objects.get(id=post_id)
    if request.method == 'POST':
      form = PostForm(request.POST,instance = post)
      if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.hood = request.user.join.hood_id
        post.save()
        return redirect('posts')
    else:
      form = PostForm(instance = post)
      return render(request,'edit_post.html',locals())

  else:
    messages.error(request,'You cannot edit this post...Join a neighbourhood first')
    return HttpResponseRedirect(request.META.get('HTTP REFERER'))

def delete_post(request,post_id):
  '''
  View function that enables a post to be deleted
  '''
  Posts.objects.filter(pk=post_id).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def add_business(request):
	'''
	View function that enables users to add businesses
	'''
	if request.method == 'POST':
		form = AddBusinessForm(request.POST)
		if form.is_valid():
			business = form.save(commit = False)
			business.user = request.user
			business.save()
			messages.success(request, 'You Have succesfully created a hood.You may now join your neighbourhood')
			return redirect('added_businesses')

	else:
		form = AddBusinessForm()
		return render(request,'add_business.html',locals())

@login_required(login_url='/accounts/login/')
def added_businesses(request):
	'''
	View function that returns all added user businesses
	'''
	businesses= Business.objects.filter(user = request.user)
	return render(request,'businesses.html',locals())

@login_required(login_url='/accounts/login/')
def edit_business(request,business_id):
	'''
	View function that enables a user to edit his/her added businesses
	'''
	business = Business.objects.get(pk = business_id)
	if request.method == 'POST':
		form = AddBusinessForm(request.POST,instance = business)
		if form.is_valid():
			form.save()
			return redirect('added_businesses')
	else:
		form = AddBusinessForm(instance = business)
	return render(request,'edit_business.html',locals())
