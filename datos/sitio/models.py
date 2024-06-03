from django.db import models

# Create your models here.
class School(models.Model):
    DBN = models.CharField(max_length=200)
    School_Name = models.CharField(default=0, max_length=200) 
    Number_of_Test_Takers = models.IntegerField(default=0) 
    Critical_Reading_Mean = models.IntegerField(default=0) 
    Mathematics_Mean = models.IntegerField(default=0) 
    Writing_Mean = models.IntegerField(default=0) 
    Average_Score = models.FloatField(default=0)
    def __str__(self):
        return self.School_Name
