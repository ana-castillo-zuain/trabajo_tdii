from django.urls import path
from sitio import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='view_data'),
    path('data/tabla/', views.tabla, name='tabla'),
    path('data/top10gral/', views.top10, name='top10'),
    path('data/top10asig/', views.top10asig, name='top10asig'),
    path('data/graficos/', views.graficos, name='graficos'),
    path('data/corr/', views.correlacion , name='correlacion' ),
    path('data/descripcion/', views.descripcion, name='desc')
]