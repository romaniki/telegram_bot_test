from rest_framework import serializers, fields

from users.models import Profile, MY_CHOICES

class ProfileSerializer(serializers.ModelSerializer):
    answer = serializers.MultipleChoiceField(choices=MY_CHOICES)
    class Meta:
        model = Profile
        fields = ['chat_id', 'tg_login', 'name', 'phone_number', 'answer']


