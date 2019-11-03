from rest_framework import serializers
import requests, os
from django.conf import settings
from .models import User, Like
from django.contrib.auth.hashers import make_password
from requests import Timeout
from decouple import config


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def check_hunter_email(self, email):
        """
        Check if email is valid using hunter.io API service
        """
        response = requests.get(
            os.getenv('HUNTER_URL', config('HUNTER_URL')) + '?email={}&api_key={}'.format(email, settings.HUNTER_KEY),
            timeout=10
        )
        data = response.json()
        if data and 'errors' not in data:
            if data['data']['result'] != 'undeliverable':
                return email
        raise serializers.ValidationError("Email does not exist")


    def create(self, validated_data):
        """
        Register user
        :param validated_data:
        :return:
        """
        password = validated_data.pop('password')
        self.check_hunter_email(validated_data['email'])
        user = User.objects.create(**validated_data)
        user.set_password(password)
        return user


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


