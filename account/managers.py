from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Extendendo base user manager para sobrescrever os metodos de crud.
    E colocar o email a ser usado no lugar de username
    """
    def create_user(self, email, cpf, full_name, password, **extra_fields):
        #lança erro (caso email esteja vazio) usando _ para tratamento de internacionalização
        if not email:
            raise ValueError('O Email deve ser informado')
        if not cpf:
            raise ValueError('O CPF deve ser informado')
        if not full_name:
            raise ValueError('O Nome Completo deve ser informado')
        # faz a normalizacao do email 
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user