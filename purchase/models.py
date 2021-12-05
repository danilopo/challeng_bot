from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Purchase(models.Model):
    
    EM_VALIDACAO = 1
    APROVADO = 2
    STATUS = [
        (EM_VALIDACAO, "Em validação"),
        (APROVADO, "Aprovado"),
    ]
    
    code = models.CharField(max_length=255)
    value = models.FloatField() 
    purchase_date = models.DateField()
    status = models.PositiveSmallIntegerField(choices=STATUS, default=EM_VALIDACAO)
    reseller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='resellers')
    
    # Um pouco de audit, nao vou remover a linha, vou fazer um soft delete 
    # atualizando para removed = True e registrar com o updated_at o momento da remocao
    # purchase_date deve registrar a data da compra mas created_at registra o tempo do update
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Period(models.Model):
    """
    Classe criada para gerenciar os periodos que irao acumular
    valores para os cashback
    """
    date_start = models.DateField()
    date_finish = models.DateField()