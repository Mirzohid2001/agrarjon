from django.urls import path
from .views import UserListAPIView, UserRegistrationAPIView,LoginAPIView
urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(),name='register'),
    path('users/', UserListAPIView.as_view(),name='users'),
    path('login/', LoginAPIView.as_view(),name='login'),
]