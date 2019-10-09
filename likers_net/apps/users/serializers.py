from rest_framework import serializers
import requests
from django.conf import settings
from .models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        response = requests.get(
            'https://api.hunter.io/v2/email-verifier?email={}&api_key={}'.format(data['email'], settings.HUNTER_KEY))
        d = response.json()
        if d and 'errors' not in d:
            if d['data']['result'] != 'undeliverable':
                return data
        raise serializers.ValidationError("Email does not exist")

    def create(self, validated_data):
        return User.objects.create(**validated_data)
