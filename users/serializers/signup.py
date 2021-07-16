""" Signup a user seralizer"""

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import password_validation
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from django.contrib.auth.models import User
from users.models import Profile

# Utilities
import jwt
from datetime import timedelta

class UsersSignupSerializer(serializers.Serializer):
    """ Handle sign in data valiation and user/profile creation """

    username = serializers.CharField(min_length=6, max_length=150, allow_blank=False,
    validators=[UniqueValidator(queryset=User.objects.all())])

    email = serializers.EmailField(max_length = 150, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(min_length=8, max_length=128, allow_blank=False)

    password_confirmation = serializers.CharField(min_length=8, max_length=128, allow_blank=False)

    def validate(self, data):
        """ Verify passwords match and not too common """
        
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValitationError({'Error':'Password does not match'})

        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        """ Handle user and profile creation """

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
        )

        profile = Profile(user=user)
        profile.is_verified=False

        profile.save()

        self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user):
        """ Send account verification link to given user """
        verification_token = self.gen_verification_token(user)
        subject = f'Welcome @{user.username}! Verify your account to start using the App'
        from_email='Application <noreply@app.com>'
        content = render_to_string (
            'emails/account_verification.html',
            {'token':verification_token, 'user':user}
        )

        msg = EmailMultiAlternatives(
            subject, content, from_email, [user.email]
        )
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token (self, user):
        """ Create a JWT token that the user can use to verify the account"""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp':int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token