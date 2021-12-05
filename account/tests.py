from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersTests(TestCase):
    # initialize the APIClient app

    def setUp(self):

        self.user = User.objects.create_user(cpf='00000000000', email='danilo@boticario.com', full_name='Danilo', password='test')
        self.user.save()
        self.user =User.objects.create_user(cpf='15350946056', email='gerente@boticario.com', full_name='Gerente Especial', password='test')
        self.user.save()
    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='boticatio@boticario.com', cpf='00011122234', full_name='Joao Lima', password='test', is_reseller=True)
        self.assertEqual(user.email, 'boticatio@boticario.com')
        self.assertTrue(user.is_active) # testa ativo
        self.assertTrue(user.is_reseller) # testa se eh revendedor
        self.assertFalse(user.is_superuser) # testa se eh superuser
        self.assertIsNone(user.username)
        #testes para lancamento de algumas excecoes
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='', password="test")
        with self.assertRaises(ValueError) as ve:
            User.objects.create_user(email='', cpf='00011122233', full_name='Danilo Oliveira', password="test")
            self.assertEquals('O Email deve ser informado',ve.message)
        with self.assertRaises(ValueError) as ve:
            User.objects.create_user(email='danilopo@gmail.com', cpf='', full_name='Danilo Oliveira', password="test")
            self.assertEquals('O CPF deve ser informado',ve.message)
        with self.assertRaises(ValueError) as ve:
            User.objects.create_user(email='danilopo@gmail.com', cpf='00011122233', full_name='', password="test")
            self.assertEquals('O Nome Completo deve ser informado',ve.message)

    def test_login(self):
        """
        Uma dúvida que fiquei foi, se o sistema irá permitir outros tipos de usuario alem de 
        revendedor, deveria fazer testes para a validacao destes outros tipos?
        ** O teste é para login mas não para login do user do tipo de revendedor ?? ** 
        """        
        self.client.login(email='danilopo@gmail.com', password='test')
        response = self.client.get(reverse('account_list_view'))
        self.assertEqual(response.status_code, 401)
        
        user = User.objects.get(email='danilo@boticario.com')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('account_list_view')) 
        self.assertEqual(response.status_code, 200)

        

