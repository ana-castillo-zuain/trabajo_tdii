from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Schools, UploadFileForm
import csv

# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("data/")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})

def handle_uploaded_file(file):
    reader = csv.reader(file)
    next(reader)
    for column in reader:
        Schools.objects.create(
            DBN = column[0],
            School_Name = column[1],
            Number_of_Test_Takers = column[2],
            Critical_Reading_Mean = column[3],
            Mathematics_Mean = column[4],
            Writing_Mean = column[5],
            )

def view_data(request):
    data = Schools.objects.all()
    return render(request, 'data.html', {'sat_data': data})
