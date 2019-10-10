from rest_framework import serializers
import requests
from django.conf import settings
from .models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate_email(self, email):
        """
        Check that start is before finish.
        """
        response = requests.get(
            'https://api.hunter.io/v2/email-verifier?email={}&api_key={}'.format(email, settings.HUNTER_KEY))
        data = response.json()
        if data and 'errors' not in data:
            if data['data']['result'] != 'undeliverable':
                return email
        raise serializers.ValidationError("Email does not exist")

    def create(self, validated_data):
        if settings.DEBUG == 1:
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
        else:
            user = User.objects.create(**validated_data)
        return user