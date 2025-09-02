from django.urls import path
from .views_ui import (
    TransactionListView, TransactionCreateView,
    TransactionUpdateView, TransactionDeleteView,
)

app_name = 'ui'

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/new/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]
