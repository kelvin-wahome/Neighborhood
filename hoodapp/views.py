from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.http import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index(request):
  '''
  View function that renders the homepage
  '''
  neighbourhoods = Neighbourhood.objects.all()
  return render(request,'index.html',locals())
