from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
#usando abstractuser ao invés de abstractbaseuser para aproveitas os campos padrao
class CustomUser(AbstractUser):
    #Apos a migration eu terei um novo user sem username, first_name e last_name
    username = None
    first_name = None
    last_name = None

    full_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(_('email address'), unique=True)
    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    #colocando uma variavel para identificar revendedores, coloquei em ingles mas 
    #nao sei se eh padrao do boticario.... 
    is_reseller = models.BooleanField(blank=True, null=True)
    # avoid removing row from database, just set 
    is_active = models.BooleanField(default=True)
    
    #com o username setado para email que foi setado como requirido mais acima
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    #aqui eu defino que os novos objetos users utlizarãos os métodos de 
    #CRUD da minha classe customizada ao invés do padrão que checa o username
    objects = CustomUserManager()

    def __str__(self):
        return self.full_name