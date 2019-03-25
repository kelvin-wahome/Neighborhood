from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.http import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Neighbourhood,Business,Profile,Join,Posts,Comments
import datetime as dt

@login_required(login_url='/accounts/login/')
def index(request):
  '''
  View function that renders the homepage
  '''
  neighbourhoods = Neighbourhood.objects.all()
  return render(request,'index.html',locals())
  
@login_required(login_url='/accounts/login/')
def search_business(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        businesses = Business.objects.filter(name__icontains = search_term,hood = request.user.join.hood_id.id)
        searched_businesses = Business.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',locals())

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',locals())
