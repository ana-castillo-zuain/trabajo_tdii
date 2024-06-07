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
from io import BytesIO
import base64
import numpy as np

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

def data(request):
    return render(request, 'data.html')

def tabla(request):
    data = School.objects.all()
    return render(request, 'tabla.html', {'data':data})

def descripcion(request):
    return render(request, 'descripcion.html')

def graficos(request):
    data = School.objects.all()
    names = [school.School_Name for school in data]
    students = [school.Number_of_Test_Takers for school in data]
    reading = [school.Critical_Reading_Mean for school in data]
    maths = [school.Mathematics_Mean for school in data]
    writing = [school.Writing_Mean for school in data]
    average_scores = [school.Average_Score for school in data]
    
    top10_average = data.order_by('-Average_Score')[:20]
    school_nameso = [school.School_Name for school in top10_average]
    average = [school.Average_Score for school in top10_average]
    plt.figure(figsize=(15, 6))
    plt.barh(school_nameso, average, color='khaki')
    plt.xlabel('Nota Promedio')
    plt.yticks(rotation=45, ha='right')
    plt.title('Top 10 Colegios segun Nota Promedio General')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    avg_png = buffer.getvalue()
    buffer.close()
    avg_graphic = base64.b64encode(avg_png)
    avg_graphic = avg_graphic.decode('utf-8')

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
    plt.figure(figsize=(15, 6))
    plt.barh(school_names, math_means, color='firebrick')
    plt.xlabel('Nota Promedio en Matemáticas')
    plt.yticks(rotation=45, ha='right')
    plt.title('Top 10 Colegios segun Nota Promedio en Matemáticas')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    math_png = buffer.getvalue()
    buffer.close()
    math_graphic = base64.b64encode(math_png)
    math_graphic = math_graphic.decode('utf-8')

    top10_reading = data.order_by('-Critical_Reading_Mean')[:20]
    school_namesr = [school.School_Name for school in top10_reading]
    read_means = [school.Critical_Reading_Mean for school in top10_reading]
    plt.figure(figsize=(15, 6))
    plt.barh(school_namesr, read_means, color='mediumseagreen')
    plt.xlabel('Nota Promedio en Lectura Crítica')
    plt.yticks(rotation=45, ha='right')
    plt.title('Top 10 Colegios segun Nota Promedio en Lectura Crítica')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    reading_png = buffer.getvalue()
    buffer.close()
    reading_graphic = base64.b64encode(reading_png)
    reading_graphic = reading_graphic.decode('utf-8')

    top10_writing = data.order_by('-Writing_Mean')[:20]
    school_namesw = [school.School_Name for school in top10_writing]
    writing_means = [school.Writing_Mean for school in top10_writing]
    plt.figure(figsize=(15, 6))
    plt.barh(school_namesw, writing_means, color='skyblue')
    plt.xlabel('Nota Promedio de Escritura')
    plt.yticks(rotation=45, ha='right')
    plt.title('Top 10 Colegios segun Nota Promedio en Escritura')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    writing_png = buffer.getvalue()
    buffer.close()
    writing_graphic = base64.b64encode(writing_png)
    writing_graphic = writing_graphic.decode('utf-8')

    plt.figure(figsize=(10, 6))
    sns.histplot(average_scores, bins=50, kde=True, color='crimson', edgecolor='black')
    plt.xlabel('Nota Promedio')
    plt.ylabel('Cantidad de Colegios')
    plt.title('Distribucion de Notas Promedio')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    hist_png = buffer.getvalue()
    buffer.close()
    hist_graphic = base64.b64encode(hist_png)
    hist_graphic = hist_graphic.decode('utf-8')

    scores = {'Critical Reading': reading, 'Mathematics': maths, 'Writing': writing, 'Average':average_scores}
    subjects = []
    marks = []
    for subject, scores_list in scores.items():
        subjects.extend([subject] * len(scores_list))
        marks.extend(scores_list)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x=subjects, y=marks)
    plt.xlabel('Asignaturas')
    plt.ylabel('Notas')
    plt.title('Boxplot de Notas para cada Asignatura')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    box_png = buffer.getvalue()
    buffer.close()
    box_graphic = base64.b64encode(box_png)
    box_graphic = box_graphic.decode('utf-8')

    scores_data = {
        'Critical_Reading_Mean': reading,
        'Mathematics_Mean': maths,
        'Writing_Mean': writing,
        'Number_of_Test_Takers': students
    }

    correlation_matrix = np.corrcoef([
        scores_data['Critical_Reading_Mean'],
        scores_data['Mathematics_Mean'],
        scores_data['Writing_Mean'],
        scores_data['Number_of_Test_Takers']
    ])
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', xticklabels=['Lectura Crítica', 'Matematica', 'Escritura', 'Cantidad de Estudiantes'], yticklabels=['Lectura Crítica', 'Matematica', 'Escritura', 'Cantidad de Estudiantes'])
    plt.title('Matriz de Correlación entre Cantidad de Estudiantes y Asignaturas')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    heat_png = buffer.getvalue()
    buffer.close()
    heat_graphic = base64.b64encode(heat_png)
    heat_graphic = heat_graphic.decode('utf-8')

    context = {
        'data': data,
        'statistics': statistics,
        'average': avg_graphic,
        'math' : math_graphic,
        'reading' : reading_graphic,
        'writing' : writing_graphic,
        'hist' : hist_graphic,
        'box' : box_graphic,
        'heat' : heat_graphic
    }

    return render(request, 'graficos.html', context)
