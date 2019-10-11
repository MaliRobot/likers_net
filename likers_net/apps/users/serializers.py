from rest_framework import serializers
import requests
from django.conf import settings
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate_email(self, email):
        """
        Check that start is before finish.
        """
        if settings.DEBUG == 0:
            response = requests.get(
                'https://api.hunter.io/v2/email-verifier?email={}&api_key={}'.format(email, settings.HUNTER_KEY))
            data = response.json()
            if data and 'errors' not in data:
                if data['data']['result'] != 'undeliverable':
                    return email
            raise serializers.ValidationError("Email does not exist")
        return email

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})
        return user