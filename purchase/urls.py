from django.urls import path
from .views import ( PurchaseListCreate, 
                        PurchaseRetrieveUpdateDelete, 
                        PurchaseStatusEdit, 
                        PurchaseListByReseller, 
                        PeriodListCreate, 
                        PeriodRetrieveUpdateDelete, 
                        TotalCashBack
                    )
urlpatterns = [
    #compras
    path('', PurchaseListCreate.as_view(), name='purchase_list_view'),
    path('<int:purchase_id>/', PurchaseRetrieveUpdateDelete.as_view(), name='purchase_detail'),
    path('list/<slug:cpf>/', PurchaseListByReseller.as_view(), name='purchase_list_by_reseller'),
    #rota para editar status 
    path('edit_status/<int:purchase_id>/', PurchaseStatusEdit.as_view(), name='purchase_status_edit'),
    #chamada externa
    path('total_cashback/<slug:cpf>/', TotalCashBack.as_view(), name='cashback_amount'),
    #urls para gerenciar periodos 
    path('periods/', PeriodListCreate.as_view(), name='period_list'),
    path('periods/<int:period_id>/', PeriodRetrieveUpdateDelete.as_view(), name='period_detail'),
]