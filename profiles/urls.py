from django.urls import path

from .views import UserProfileDetailView, profile_update_view

app_name = 'profiles'

urlpatterns = [
    path('<int:pk>/',
        UserProfileDetailView.as_view(),
        name='profile_detail'),

    path('update/<int:pk>/', 
        profile_update_view,
        name = 'profile_update')
]