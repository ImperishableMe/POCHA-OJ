from django.urls import path
from .views import ProblemCreateView,ProblemUpdateView,ProbleAddTestCaseView
app_name = 'newProblems'

urlpatterns = [
    path('',ProblemCreateView.as_view(),name='create_problem'),   
    path('update/<int:pk>',ProblemUpdateView.as_view(),name='update_problem'),   
    path('addTestCase/<int:pid>',ProbleAddTestCaseView.as_view(),name='add_testcase'),   
]
