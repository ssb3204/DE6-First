from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('search/', views.search_page, name='search_page'),
    path('datalist/', views.import_jobs_csv,name='datalist'),

]
