from django.urls import path
from sitio import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('data/', views.data, name='view_data'),
    path('data/tabla/', views.tabla, name='tabla'),
    path('data/graficos/', views.graficos, name='graficos')
]