from django.urls import path
from . import views
app_name = 'problem'

urlpatterns = [
    path('',views.ProblemListView.as_view(),name='problem_list'),
    path('<int:pk>/detail/',views.ProblemDetailView.as_view(),name='problem_detail'),

]
