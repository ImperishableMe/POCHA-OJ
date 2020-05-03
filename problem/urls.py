from django.urls import path
from . import views
app_name = 'problem'

urlpatterns = [
    path('',views.ProblemListView.as_view(),name='problem_list'),
    path('<int:pk>/detail/',views.ProblemDetailView.as_view(),name='problem_detail'),
    path('<int:pid>/submit/',views.SubmitView.as_view(),name='submit'),    
    path('submission_list/',views.SubmissionListView.as_view(),name='submission_list'),
]
