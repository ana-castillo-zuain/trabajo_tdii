from django.urls import path
from sitio import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='view_data'),
    path('data/tabla/', views.tabla, name='tabla'),
    path('data/graficos/', views.graficos, name='graficos'),
    path('data/descripcion/', views.descripcion, name='desc')
]