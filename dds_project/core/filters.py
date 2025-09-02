import django_filters as df
from .models import Transaction

class TransactionFilter(df.FilterSet):
    date_from = df.DateFilter(field_name='date', lookup_expr='gte')
    date_to = df.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = {
            'status': ['exact'],
            'type': ['exact'],
            'category': ['exact'],
            'subcategory': ['exact'],
        }
