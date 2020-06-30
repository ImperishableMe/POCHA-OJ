from django.urls import path
from .views import ProblemCreateView
app_name = 'newProblems'

urlpatterns = [
    path('',ProblemCreateView.as_view(),name='create_problem'),   
]
