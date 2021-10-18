from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>', views.ProfileAPIView.as_view(), name="profile-detail"),
    path('profile', views.ProfileCreate.as_view(), name="profile-create")
]
