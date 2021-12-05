import requests
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, generics
from .models import Purchase, Period
from django.core.exceptions import ValidationError
from .serializers import (
        PurchaseSerializer, 
        PurchaseStatusSerializer,
        PeriodSerializer, 
        PurchaseListSerializer
    )   
class TotalCashBack(APIView):
    """
    Class based view que trata a chama externa 
    usei requests para fazer as chamadas
    """
    def get(self, request, cpf):
        url = settings.URL
        params = {
            'cpf':cpf
        }
        headers={
            "token":settings.TOKEN
        }
        response = requests.get(url,headers=headers, params=params)
        return Response(response.json(), status=status.HTTP_200_OK) 

class PeriodRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    lookup_url_kwarg = 'period_id'

class PeriodListCreate(generics.ListCreateAPIView):
    queryset = Period.objects.all() # devido ao soft delete, listar apenas as que não foram removidas(ativas)
    serializer_class = PeriodSerializer

class PurchaseListByReseller(generics.ListAPIView):
    serializer_class = PurchaseListSerializer
    
    def get_queryset(self):
        return Purchase.objects.filter(status=Purchase.APROVADO, reseller__cpf=self.kwargs['cpf'])

class PurchaseStatusEdit(generics.UpdateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseStatusSerializer
    lookup_url_kwarg = 'purchase_id'

class PurchaseListCreate(generics.ListCreateAPIView):
    queryset = Purchase.objects.filter(removed=False) # devido ao soft delete, listar apenas as que não foram removidas(ativas)
    serializer_class = PurchaseSerializer

class PurchaseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.filter(removed=False) # nao trazer na consulta os removidos (apenas ativos)
    serializer_class = PurchaseSerializer
    lookup_url_kwarg = 'purchase_id'

    #override do metodo delete para tratar apenas em validação
    #soft delete - inativar a compra
    def destroy(self, request, *args, **kwargs):
        purchase = Purchase.objects.get(id=self.kwargs['purchase_id'])
        if purchase.status == Purchase.APROVADO:
            return Response(
                {'Não é permitido a exclusão se a compra já está aprovada'},status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        purchase.removed = True
        purchase.save()
        return Response({
                'Exclusão realizada com sucesso'},status.HTTP_200_OK
        )
    #permission_classes = [permissions.AllowAny]
