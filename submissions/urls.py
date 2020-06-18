from django.urls import path
from .views  import SubmitView,SubmissionListView,SubmissionDetailView
app_name = 'submissions'

urlpatterns = [
    
    path('submit/<int:pid>/',SubmitView.as_view(),name='submit'),    
    path('submission_list/',SubmissionListView.as_view(),name='submission_list'),
    path('submission_detail/<int:pk>/', SubmissionDetailView.as_view(), name = 'submission_detail'),
    
]
