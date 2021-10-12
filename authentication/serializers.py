import enum

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.models import Hospital, User, Donor

from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




class RegistrationSerializer(serializers.ModelSerializer):
    class Roles(enum.Enum):
        DONOR = "DONOR", "Donor"
        HOSPITAL = "HOSPITAL", "Hospital"

    password = serializers.CharField(
        min_length=6, max_length=100, write_only=True
    )
    roles = [role.value for role in Roles]
    type = serializers.ChoiceField(choices=roles, required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    email = serializers.CharField(max_length=100, required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'type', ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        type = self.validated_data['type']
        if type == 'DONOR':
            user = Donor.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                password=validated_data['password'],
                type=type,
                is_active=True
            )
        elif type == 'HOSPITAL':
            user = Hospital.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                password=validated_data['password'],
                type=type,
                is_active=True
            )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.type
        token['username'] = user.username

        return token

class ResetPasswordEmailRequest(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=64, write_only= True)
    token = serializers.CharField(min_length=1, write_only= True)
    uidb64 = serializers.CharField(min_length=1, write_only= True)

    class Meta:
        fields = ['password', 'token','uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The token is invalid', 401)

            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The token is invalid', 401)
        return super().validate(attrs)