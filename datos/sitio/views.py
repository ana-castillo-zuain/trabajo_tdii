from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from .models import School
from django.db.models import Avg, Max, Min
import csv
import matplotlib.pyplot as plt 
import os
import seaborn as sns

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
                School_Name = row[1],
                Number_of_Test_Takers = number_of_test_takers,
                Critical_Reading_Mean = critical_reading_mean,
                Mathematics_Mean = mathematics_mean,
                Writing_Mean = writing_mean,
                Average_Score = average_score
            )
    return HttpResponseRedirect('data/')


def view_data(request):
    data = School.objects.all()
    names = [school.School_Name for school in data]
    students = [school.Number_of_Test_Takers for school in data]
    reading = [school.Critical_Reading_Mean for school in data]
    maths = [school.Mathematics_Mean for school in data]
    writing = [school.Writing_Mean for school in data]
    average_scores = [school.Average_Score for school in data]

    static_dir = os.path.join(settings.STATIC_ROOT, 'images')
    
    top10_average = data.order_by('-Average_Score')[:20]
    school_nameso = [school.School_Name for school in top10_average]
    average = [school.Average_Score for school in top10_average]
    plt.figure(figsize=(10, 6))
    plt.barh(school_nameso, average, color='orange')
    plt.xlabel('Average Score')
    plt.title('Top 5 Schools by Average Score')
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

    top10_maths = data.order_by('-Mathematics_Mean')[:20]
    school_names = [school.School_Name for school in top10_maths]
    math_means = [school.Mathematics_Mean for school in top10_maths]
    plt.figure(figsize=(10, 6))
    plt.barh(school_names, math_means, color='maroon')
    plt.xlabel('Mathematics Mean Score')
    plt.title('Top 3 Schools by Mathematics Mean Score')
    plt.gca().invert_yaxis()
    math_image_path = os.path.join(static_dir, 'top10maths.png')
    plt.savefig(math_image_path)
    plt.close()

    top10_reading = data.order_by('-Critical_Reading_Mean')[:20]
    school_namesm = [school.School_Name for school in top10_reading]
    math_means = [school.Critical_Reading_Mean for school in top10_reading]
    plt.figure(figsize=(10, 6))
    plt.barh(school_namesm, math_means, color='seagreen')
    plt.xlabel('Critical Reading Mean Score')
    plt.title('Top 3 Schools by Critical Reading Mean Score')
    plt.gca().invert_yaxis()
    reading_image_path = os.path.join(static_dir, 'top10reading.png')
    plt.savefig(reading_image_path)
    plt.close()

    top10_writing = data.order_by('-Writing_Mean')[:20]
    school_namesw = [school.School_Name for school in top10_writing]
    writing_means = [school.Writing_Mean for school in top10_writing]
    plt.figure(figsize=(10, 6))
    plt.barh(school_namesw, writing_means, color='skyblue')
    plt.xlabel('Critical Reading Mean Score')
    plt.title('Top 3 Schools by Writing Mean Score')
    plt.gca().invert_yaxis()
    writing_image_path = os.path.join(static_dir, 'top10writing.png')
    plt.savefig(writing_image_path)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.histplot(average_scores, bins=50, kde=True, color='slateblue', edgecolor='black')
    plt.xlabel('Average Score')
    plt.ylabel('Number of Schools')
    plt.title('Distribution of Average Scores')
    histogram_path = os.path.join(static_dir, 'average_score_histogram.png')
    plt.savefig(histogram_path)
    plt.close()

    scores = {'Critical Reading': reading, 'Mathematics': maths, 'Writing': writing, 'Average':average_scores}
    subjects = []
    marks = []
    for subject, scores_list in scores.items():
        subjects.extend([subject] * len(scores_list))
        marks.extend(scores_list)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x=subjects, y=marks)
    plt.xlabel('Subject')
    plt.ylabel('Scores')
    plt.title('Boxplot of Scores in Each Subject')
    boxplot_path = os.path.join(static_dir, 'subjects_boxplot.png')
    plt.savefig(boxplot_path)
    plt.close()

    context = {
        'data': data,
        'statistics': statistics,
        'math': 'images/top10maths.png',
        'reading': 'images/top10reading.png',
        'writing': 'images/top10writing.png',
        'average': 'images/top10average.png',
        'histogram': 'images/average_score_histogram.png',
        'boxplot' : 'images/subjects_boxplot.png'
    }

    return render(request, 'data.html', context)
