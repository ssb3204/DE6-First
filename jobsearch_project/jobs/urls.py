from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_page, name='search_page'),
    path('datalist/', views.import_jobs_csv,name='datalist'),
]
