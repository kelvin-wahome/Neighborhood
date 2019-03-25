from django.db import models
import datetime as dt
from django.contrib.auth.models import User



class Neighbourhood(models.Model):
  '''
  class that contains Neighbourhood properties
  '''
  NEIGHBOURHOOD_CHOICES = (
    ('South B','South B'),
    ('South C','South C'),
    ('Westlands','Westlands'),
    ('Donholm','Donholm'),
    ('Ruaka','Ruaka'),
    ('Imara Daima','Imara Daima'),
    ('Syokimau','Syokimau'),
    ('Buruburu','Buruburu'),
    ('Kinoo','Kinoo'),
    ('Komarock','Komarock'),
    ('Madaraka','Madaraka'),
    ('Rongai','Rongai'),
    ('Karen','Karen'),
    ('Ruiru','Ruiru'),
    ('Roysambu','Roysambu'),
    ('Juja','Juja'),
  )
  name = models.CharField(max_length=200)
  location = models.CharField(max_length=30,choices=NEIGHBOURHOOD_CHOICES)
  description = models.TextField(blank=True,null=True)
  posted_on = models.DateTimeField(auto_now_add=True)
  police_dept = models.IntegerField(default="0722445233")
  health_dept = models.IntegerField(default="0700505221")
  user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
