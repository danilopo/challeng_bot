from .models import Purchase, Period
from django.db.models import Q, Sum
from django.conf import settings
def get_cashback_percentual(purchase):
    #identificacao do periodo (duvida: se houver periodos intercalados???? Estou desconsiderando esses casos)
    period = Period.objects.filter(Q(date_start__lte=purchase.purchase_date) & Q (date_finish__gte=purchase.purchase_date)).first()
    purchases_amount = Purchase.objects.filter(status=Purchase.APROVADO,
                                                reseller=purchase.reseller,
                                                purchase_date__range=[period.date_start,period.date_finish]).aggregate(Sum('value'))['value__sum']
    ##  
    if purchases_amount < settings.LOW_OFF_CEIL:
        return 0.1
    elif purchases_amount <= settings.MID_OFF_CEIL:
        return 0.15
    else:
        return 0.2