import random
import string

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, 8))

    queryset = CustomUser.objects.all()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=queryset)],
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            raise serializers.ValidationError(
                "Нельзя называть пользователя me"
            )
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=self.rand_string,
            confirmation_code=self.rand_string
        )

        user.save()
        send_mail(
            'Register code',
            f'{self.rand_string}',
            'postmaster@sandboxd3d1ea751b8f42b395f3368371a3840c.mailgun.org',
            [validated_data['email']]
        )
        return user


class TokenSerializer(TokenObtainPairSerializer):
    password = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('password', 'username',)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
        }
