from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
  url('^$',views.index,name = 'index'),
   url(r'^add_hood/$', views.add_hood, name='add_hood'),
  url(r'^join/(\d+)',views.join_hood,name='join_hood'),
  url(r'^profile/$',views.profile,name = 'profile'),
  url(r'^update_profile/$',views.update_profile,name= 'update_profile'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
