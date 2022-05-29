from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Lable(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null =True )
    lable = models.CharField( max_length=200)
    update = models.DateField( auto_now=True)
    create =models.DateField(auto_now_add=True)
    
    class Meta:
        ordering=['-update','-create']

    def __str__(self):
        return self.lable

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    lable = models.ForeignKey(Lable, on_delete=models.CASCADE)
    note = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note