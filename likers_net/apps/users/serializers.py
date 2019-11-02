from rest_framework import serializers
import requests
from django.conf import settings
from .models import User, Like
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate_email(self, email):
        """
        Check if email is valid using hunter.io API service
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
        """
        Register user
        :param validated_data:
        :return:
        """
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        return user


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


