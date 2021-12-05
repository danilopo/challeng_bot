from django.urls import path
from .views import UserListCreate, UserRetrieveUpdateDelete

urlpatterns = [
    path('', UserListCreate.as_view(), name='account_list_view'),
    path('<int:user_id>/', UserRetrieveUpdateDelete.as_view(), name='account_edit')
]