from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import F, ExpressionWrapper, FloatField
from .models import School
import csv
import matplotlib.pyplot as plt 

# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload_file(request):
    with open (staticfiles_storage.path('dataset.csv'), 'r') as file:
        reader = csv.reader(file)
        reader.__next__()
        for row in reader:
            School.objects.create(
                 DBN = row[0],
                 School_Name = row[1],
                 Number_of_Test_Takers = row[2],
                 Critical_Reading_Mean = row[3],
                 Mathematics_Mean = row[4],
                 Writing_Mean = row[5],
                 )
    return HttpResponseRedirect('data/')


def view_data(request):
    data = School.objects.all()
    # School.objects.annotate(
    #     Average_Score=ExpressionWrapper(
    #         (F('Critical_Reading_Mean')+F('Mathematics_Mean')+F('Writing_Mean'))
    #         /3.00, output_field=FloatField()
    #         )
    #     )
    # names = [data.School_Name for data in data]
    # students = [data.Number_of_Test_Takers for data in data]
    # reading = [data.Critical_Reading_Mean for data in data]
    # maths = [data.Mathematics_Mean for data in data]
    # writing = [data.Writing_Mean for data in data]
    # avg = [data.Average_Score for data in data]
    sample_schools = data[:10]
    top10_maths = data.order_by('-Mathematics_Mean')[:10]
    school_names = [school.School_Name for school in top10_maths]
    math_means = [school.Mathematics_Mean for school in top10_maths]
    plt.figure(figsize=(10, 6))
    plt.barh(school_names, math_means, color='crimson')
    plt.xlabel('Mathematics Mean Score')
    plt.title('Top 10 Schools by Mathematics Mean Score')
    plt.gca().invert_yaxis()
    plt.savefig('top10maths.png')

    top10_reading = data.order_by('-Critical_Reading_Mean')[:10]
    school_namesm = [school.School_Name for school in top10_reading]
    math_means = [school.Critical_Reading_Mean for school in top10_reading]
    plt.figure(figsize=(10, 6))
    plt.barh(school_namesm, math_means, color='crimson')
    plt.xlabel('Critical Reading Mean Score')
    plt.title('Top 10 Schools by Critical Reading Mean Score')
    plt.gca().invert_yaxis()
    plt.savefig('top10reading.png')

    top10_writing = data.order_by('-Writing_Means')[:10]
    school_namesw = [school.School_Name for school in top10_writing]
    writing_means = [school.Critical_Reading_Mean for school in top10_writing]
    plt.figure(figsize=(10, 6))
    plt.barh(school_namesw, writing_means, color='skyblue')
    plt.xlabel('Critical Reading Mean Score')
    plt.title('Top 10 Schools by Writing Mean Score')
    plt.gca().invert_yaxis()
    plt.savefig('top10writing.png')

    return render(request, 'data.html', {'data': data })
