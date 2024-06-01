from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage

from .models import School
import csv

# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload_file(request):
    with open (staticfiles_storage.path('dataset.csv'), 'r') as file:
        reader = csv.reader(file)
        reader.__next__()
        rowaux = []
        for row in reader:
            print(row)
            rowaux = row
            # School.objects.create(
            #     DBN = row[0],
            #     School_Name = row[1],
            #     Number_of_Test_Takers = row[2],
            #     Critical_Reading_Mean = row[3],
            #     Mathematics_Mean = row[4],
            #     Writing_Mean = row[5],
            #     )
    # return HttpResponseRedirect('data/')
    return render(rowaux)

def view_data(request):
    data = School.objects.all()
    return render(request, 'data.html', {'data':data})
