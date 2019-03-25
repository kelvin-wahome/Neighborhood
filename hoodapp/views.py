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
