from django.urls import path
from . import views
urlpatterns = [
    path('<str:company_id>/', views.allJobs, name='allJobs'),
    path('<str:id>/add-job', views.addJob, name="addJob")

    
]