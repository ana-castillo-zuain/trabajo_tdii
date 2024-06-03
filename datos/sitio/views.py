from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from .models import School
from django.db.models import Avg, Max, Min
import csv
import matplotlib.pyplot as plt 
import os

# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload_file(request):
    with open (staticfiles_storage.path('dataset.csv'), 'r') as file:
        reader = csv.reader(file)
        reader.__next__()
        for row in reader:
            number_of_test_takers = int(row[2])
            critical_reading_mean = int(row[3])
            mathematics_mean = int(row[4])
            writing_mean = int(row[5])
            average_score = (critical_reading_mean + mathematics_mean + writing_mean) / 3
            School.objects.create(
                DBN=row[0],
                School_Name=row[1],
                Number_of_Test_Takers=number_of_test_takers,
                Critical_Reading_Mean=critical_reading_mean,
                Mathematics_Mean=mathematics_mean,
                Writing_Mean=writing_mean,
                Average_Score=average_score
            )
    return HttpResponseRedirect('data/')


def view_data(request):
    data = School.objects.all()
    # names = [data.School_Name for data in data]
    # students = [data.Number_of_Test_Takers for data in data]
    # reading = [data.Critical_Reading_Mean for data in data]
    # maths = [data.Mathematics_Mean for data in data]
    # writing = [data.Writing_Mean for data in data]
    # avg = [data.Average_Score for data in data]
    sample_schools = data[:10]

    static_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    top10_average = data.order_by('-Average_Scores')[:10]
    school_nameso = [school.School_Name for school in top10_average]
    average = [school.Average_Score for school in top10_average]
    plt.figure(figsize=(10, 6))
    plt.barh(school_nameso, average, color='orange')
    plt.xlabel('Average Score')
    plt.title('Top 10 Schools by Average Score')
    plt.gca().invert_yaxis()
    average_image_path = os.path.join(static_dir, 'top10average.png')
    plt.savefig(average_image_path)
    plt.close()

    statistics = {
        'Critical Reading': {
            'average': School.objects.all().aggregate(Avg('Critical_Reading_Mean'))['Critical_Reading_Mean__avg'],
            'max': School.objects.all().aggregate(Max('Critical_Reading_Mean'))['Critical_Reading_Mean__max'],
            'min': School.objects.all().aggregate(Min('Critical_Reading_Mean'))['Critical_Reading_Mean__min'],
        },
        'Mathematics': {
            'average': School.objects.all().aggregate(Avg('Mathematics_Mean'))['Mathematics_Mean__avg'],
            'max': School.objects.all().aggregate(Max('Mathematics_Mean'))['Mathematics_Mean__max'],
            'min': School.objects.all().aggregate(Min('Mathematics_Mean'))['Mathematics_Mean__min'],
        },
        'Writing': {
            'average': School.objects.all().aggregate(Avg('Writing_Mean'))['Writing_Mean__avg'],
            'max': School.objects.all().aggregate(Max('Writing_Mean'))['Writing_Mean__max'],
            'min': School.objects.all().aggregate(Min('Writing_Mean'))['Writing_Mean__min'],
        }
    }

    top10_maths = data.order_by('-Mathematics_Mean')[:10]
    school_names = [school.School_Name for school in top10_maths]
    math_means = [school.Mathematics_Mean for school in top10_maths]
    plt.figure(figsize=(10, 6))
    plt.barh(school_names, math_means, color='maroon')
    plt.xlabel('Mathematics Mean Score')
    plt.title('Top 10 Schools by Mathematics Mean Score')
    plt.gca().invert_yaxis()
    math_image_path = os.path.join(static_dir, 'top10maths.png')
    plt.savefig(math_image_path)
    plt.close()

    top10_reading = data.order_by('-Critical_Reading_Mean')[:10]
    school_namesm = [school.School_Name for school in top10_reading]
    math_means = [school.Critical_Reading_Mean for school in top10_reading]
    plt.figure(figsize=(10, 6))
    plt.barh(school_namesm, math_means, color='seagreen')
    plt.xlabel('Critical Reading Mean Score')
    plt.title('Top 10 Schools by Critical Reading Mean Score')
    plt.gca().invert_yaxis()
    math_image_path = os.path.join(static_dir, 'top10maths.png')
    plt.savefig(math_image_path)
    plt.close()

    top10_writing = data.order_by('-Writing_Means')[:10]
    school_namesw = [school.School_Name for school in top10_writing]
    writing_means = [school.Writing_Mean for school in top10_writing]
    plt.figure(figsize=(10, 6))
    plt.barh(school_namesw, writing_means, color='skyblue')
    plt.xlabel('Critical Reading Mean Score')
    plt.title('Top 10 Schools by Writing Mean Score')
    plt.gca().invert_yaxis()
    writing_image_path = os.path.join(static_dir, 'top10writing.png')
    plt.savefig(writing_image_path)
    plt.close()

    context = {
        'data': data,
        'statistics': statistics,
        'math_image': 'images/top10maths.png',
        'reading_image': 'images/top10reading.png',
        'writing_image': 'images/top10writing.png',
        'average_image': 'images/top10average.png'
    }

    return render(request, 'data.html', context)
