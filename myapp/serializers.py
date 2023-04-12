from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueTogetherValidator


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class ArcticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arcticle
        fields = '__all__'

# class ArcticleCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Arcticle
#         fields = ['name', 'text', 'author']

class ArcticleCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Arcticle
        fields = ['name', 'text', 'author_id']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
