from django.urls import path
from finance.views.transaction_for_click import TransactionForClickListView
from finance.views.transaction_payme import TransactionPaymeListView


urlpatterns = [
    # Payme
    path('transaction-payme/', TransactionPaymeListView.as_view(), name='transaction-payme-detail'),

    path('transaction-for-click/', TransactionForClickListView.as_view(), name='transaction-for-click'),
]
