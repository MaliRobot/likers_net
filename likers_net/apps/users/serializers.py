from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
import requests
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8)
    birthdate = serializers.DateField(read_only=True)

    def create(self, validated_data):
        """
        Check if email address is valid before saving user
        :param validated_data:
        :return:
        """
        email = validated_data['email']
        response = requests.get('https://api.hunter.io/v2/email-verifier?email={}&api_key={}'.format(email, settings.HUNTER_KEY))
        data = response.json()
        if data and 'errors' not in data:
            if data['data']['result'] != 'undeliverable':
                user = User(
                    email=email,
                    username=validated_data['username'],
                )
                user.set_password(validated_data['password'])
                user.is_staff = True
                user.save()
                return user
            raise serializers.ValidationError('Email address is not valid.')
        raise serializers.ValidationError('Cannot verify email address, try again later.')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'bio', 'location', 'birthdate')