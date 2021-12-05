from rest_framework import serializers
from .models import Purchase, Period
from django.contrib.auth import get_user_model
from django.conf import settings
from .utils import get_cashback_percentual

class PurchaseListSerializer(serializers.ModelSerializer):
    
    cashback_percent = serializers.SerializerMethodField()
    cashback_value = serializers.SerializerMethodField()

    def get_cashback_percent(self, obj):
        return get_cashback_percentual(obj)

    def get_cashback_value(self, obj):
        percent = get_cashback_percentual(obj)
        return obj.value * percent

    class Meta:
        model = Purchase
        fields = ['code','value', 'purchase_date', 'reseller', 'status', 'cashback_percent', 'cashback_value']


class PurchaseStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Purchase
        fields = ['status']

class PurchaseSerializer(serializers.ModelSerializer):
    User = get_user_model()
    reseller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.CharField(source='get_status_display', read_only=True)
    def validate(self, data):
        #update apenas permitir editar apenas se o status da venda for “Em validação”;
        if self.instance:
            purchase = Purchase.objects.get(id=self.instance.id)
            if purchase.status == Purchase.APROVADO:
                raise serializers.ValidationError('Compra possui status Aprovado')
        #Se o revendedor tem o super cpf altera para aprovado diretamentee
        if data['reseller'].cpf == settings.REVENDEDOR_ESPECIAL:
            data.update({"status": Purchase.APROVADO})
        return super().validate(data)

    class Meta:
        model = Purchase
        fields = ['id', 'code','value', 'purchase_date', 'reseller', 'status']

class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = '__all__'