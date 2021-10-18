from rest_framework import generics

from users.models import Profile
from .serializers import ProfileSerializer
''' API ENDPOINTS '''

class ProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileCreate(generics.CreateAPIView):
    serializer_class = ProfileSerializer
