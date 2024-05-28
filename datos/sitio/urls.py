from django.urls import path
from sitio import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('data/', views.view_data, name='view_data'),
]