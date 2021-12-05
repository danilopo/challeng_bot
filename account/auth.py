
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email, password, **kwargs):
        try:
            # consulta pelo email se a pessoa já existe 
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return
        #se usuario existe entao faz ultima verificacao de email 
        if user.check_password(password) and self.user_can_authenticate(user):
            return user