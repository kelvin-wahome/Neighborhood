from django.db import models
import datetime as dt
from django.contrib.auth.models import User


class Neighbourhood(models.Model):
    '''
    class that contains Neighbourhood properties
    '''
    NEIGHBOURHOOD_CHOICES = (
        ('South B', 'South B'),
        ('South C', 'South C'),
        ('Westlands', 'Westlands'),
        ('Donholm', 'Donholm'),
        ('Ruaka', 'Ruaka'),
        ('Imara Daima', 'Imara Daima'),
        ('Syokimau', 'Syokimau'),
        ('Buruburu', 'Buruburu'),
        ('Kinoo', 'Kinoo'),
        ('Komarock', 'Komarock'),
        ('Madaraka', 'Madaraka'),
        ('Rongai', 'Rongai'),
        ('Karen', 'Karen'),
        ('Ruiru', 'Ruiru'),
        ('Roysambu', 'Roysambu'),
        ('Juja', 'Juja'),
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=30, choices=NEIGHBOURHOOD_CHOICES)
    description = models.TextField(blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    police_dept = models.IntegerField(default="0722445233")
    health_dept = models.IntegerField(default="0700505221")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def save_neighbourhood(self):
        self.save()

    def update_neighbourhood(self):
        self.update()

    def update_occupants(self):
        self.update()

    def delete_neighbourhood(self):
        self.delete()

    class Meta:
        ordering = ['posted_on']

    @classmethod
    def get_neighbourhoods(cls):
        neighbourhoods = Neighbourhood.objects.all()
        return neighbourhoods

    @classmethod
    def find_neighbourhood_by_id(cls, id):
        neighbourhood = Neighbourhood.objects.get(id=id)
        return neighbourhood

    @classmethod
    def search_by_title(cls, search_term):
        neighbourhood = cls.objects.filter(name__icontains=search_term)
        return neighbourhood

    def __str__(self):
        return self.name


class Profile(models.Model):
    '''
    class that contains user Profile properties
    '''
    bio = models.TextField()
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    hood = models.OneToOneField(
        Neighbourhood, on_delete=models.CASCADE, blank=True, null=True)
