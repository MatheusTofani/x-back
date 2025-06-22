from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class User(AbstractUser):
    full_name = models.CharField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ['full_name', 'email', 'birth_date', 'password']

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.filter(email__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Esse email já está em uso por outro usuário.")
        return value

    def validate_birth_date(self, value):
        
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Você precisa ter pelo menos 18 anos.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance