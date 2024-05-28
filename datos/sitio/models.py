from django.db import models
from django import forms
# Create your models here.
class Schools(models.Model):
    DBN = models.CharField(max_length=200)
    School_Name = models.CharField(default=0, max_length=200) 
    Number_of_Test_Takers = models.IntegerField(default=0) 
    Critical_Reading_Mean = models.IntegerField(default=0) 
    Mathematics_Mean = models.IntegerField(default=0) 
    Writing_Mean = models.IntegerField(default=0) 

class UploadFileForm(forms.Form):
    file = forms.FileField()