from django.urls import path
from . import views
app_name = 'submissions'

urlpatterns = [
    
    path('submit/<int:pid>/',views.SubmitView.as_view(),name='submit'),    
    path('submission_list/',views.SubmissionListView.as_view(),name='submission_list'),
]
