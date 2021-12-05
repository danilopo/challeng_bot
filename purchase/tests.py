import json
import datetime 
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase, Client
from django.urls import reverse
from .models import Purchase, Period
from .serializers import PurchaseSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
User = get_user_model()
client = APIClient()
class PurchaseTests(TestCase):

    def setUp(self):
        #periodos
        #outubro
        period_oct = Period(date_start=datetime.date(2021,10,1), date_finish=datetime.date(2021,10,31))
        period_oct.save()
        #novembro
        period_nov = Period(date_start=datetime.date(2021,11,1) , date_finish=datetime.date(2021,11,30))
        period_nov.save()
        #dezembro
        period_dec = Period(date_start=datetime.date(2021,12,1) , date_finish=datetime.date(2021,12,31))
        period_dec.save()
        #usuArios
        user = User.objects.create_user(cpf='00000000000', email='danilo@boticario.com', full_name='Danilo', password='test')
        user.save()
        special_user =User.objects.create_user(cpf='15350946056', email='gerente@boticario.com', full_name='Gerente Especial', password='test')
        special_user.save()
        #esquema de compras
        #4 compras em outrubro -> 2100 reais (>2000) 0.2 cashback
        #3 compras em novembro -> 1500 reais (entre 1000 e 1500) 0.15 cashback
        #1 compra em dezembro -> 600 reais (< 1000) 0.1 cashback
        purchase1 = Purchase(code='100', value=1000, purchase_date=datetime.date(2021,10,4), status=Purchase.APROVADO, reseller=user)
        purchase1.save()
        purchase2 = Purchase(code='200', value=600, purchase_date=datetime.date(2021,10,8), status=Purchase.APROVADO, reseller=user)
        purchase2.save()
        purchase3 = Purchase(code='300', value=300, purchase_date=datetime.date(2021,10,14), status=Purchase.APROVADO, reseller=user)
        purchase3.save()
        purchase4 = Purchase(code='400', value=200, purchase_date=datetime.date(2021,10,24), status=Purchase.APROVADO, reseller=user)
        purchase4.save()

        #5 nao sera somado pois se encontrará com status em avaliacao
        purchase5 = Purchase(code='500', value=400, purchase_date=datetime.date(2021,11,5), reseller=user)
        purchase5.save()

        purchase6 = Purchase(code='600', value=500, purchase_date=datetime.date(2021,11, 8), status=Purchase.APROVADO, reseller=user)
        purchase6.save()
        purchase7 = Purchase(code='700', value=600, purchase_date=datetime.date(2021,11, 18), status=Purchase.APROVADO, reseller=user)
        purchase7.save()
        purchase8 = Purchase(code='800', value=100, purchase_date=datetime.date(2021,11, 28), status=Purchase.APROVADO, reseller=user)
        purchase8.save()

        #será cadastrado com o gerente especial, status deve ir automaticamente para aprovado
        purchase9 = Purchase(code='900', value=600, purchase_date=datetime.date(2021,12,10), reseller=special_user)
        purchase9.save()

        purchase10 = Purchase(code='1000', value=100, purchase_date=datetime.date(2021,12,11), status=Purchase.APROVADO ,reseller=user)
        purchase10.save()

    def test_status(self):
        #testa se o status foi salvo diretamente para APROVADO caso cpf seja 
        purchase = Purchase.objects.get(code='500')
        self.assertEquals(Purchase.EM_VALIDACAO, purchase.status)
        

        client.force_authenticate(user=User.objects.get(id=2))
        response = client.post('/purchase/', {
                'code': '1000',
                'value': 100,
                'purchase_date': datetime.date(2021,12,9),
                'reseller': '2', # usuario com o cpf especial, vai para aprovado direto
        }, format='json')
        data = response.json()
        self.assertEquals('Aprovado', data['status'])

    def test_edit(self):
        #compra 500 está com status validação vou alterar
        client.force_authenticate(user=User.objects.get(id=1))
        response = client.put('/purchase/5/', {
                'code': 500,
                'value': 200,
                'purchase_date': datetime.date(2021,11,5),
                'reseller': 1,
        }, format='json')
        data = response.json()
        self.assertEquals(200.0,data['value'])
        #Se aprovada nao permitir alteracao
        response = client.put('/purchase/1/', {
                'code': 600,
                'value': 200,
                'purchase_date': datetime.date(2021,11,5),
                'reseller': 1,
        }, format='json')
        self.assertEquals(response.status_code, 400) # alteracao apenas para status em validação

    def test_remove(self):
        client.force_authenticate(user=User.objects.get(id=1))
        response = client.delete('/purchase/5/', {
                'code': 500,
                'value': 200,
                'purchase_date': datetime.date(2021,11,5),
                'reseller': 1,
        }, format='json')
        self.assertEquals(200,response.status_code)
        #Se aprovada nao permitir alteracao
        response = client.delete('/purchase/1/', {
                'code': 600,
                'value': 200,
                'purchase_date': datetime.date(2021,11,5),
                'reseller': 1,
        }, format='json')
        self.assertEquals(response.status_code, 500) # remove apenas status em validação (coloquei 500 na view)
    
    def test_cashback(self):
        client.force_authenticate(user=User.objects.get(id=1))
        response = client.get('/purchase/list/00000000000/', format='json')
        data = response.json()
        print(len(data))
        #Vou escolher alguns itens da lista para testar os calculos
        #Periodo 1 - 4 compras - acumulado > 2000 - percent cashback 0.2
        compra_periodo_1 = data[0] # valor da compra 1000
        self.assertEquals(0.2, compra_periodo_1['cashback_percent'])
        self.assertEquals(200, compra_periodo_1['cashback_value'])
        #Periodo 2 - 3 compras - 1000 < acumulado < 1500 - percent cashback 0.15
        compra_periodo_2 = data[5]
        self.assertEquals(0.15, compra_periodo_2['cashback_percent'])
        self.assertEquals(90, compra_periodo_2['cashback_value'])
        #Periodo 3 - 1 compra - 100 - acumulado < 1000 - percent cashback 0.1
        compra_periodo_3 = data[7]
        self.assertEquals(0.1, compra_periodo_3['cashback_percent'])
        self.assertEquals(10, compra_periodo_3['cashback_value'])





