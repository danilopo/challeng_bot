from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):

    #verifiquei que o serializer esta salvando a senha em plain text
    #usando o validate para fazer hash da senha
    def validate_password(self, value):
        return make_password(value)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'cpf','email', 'password']