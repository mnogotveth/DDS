from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import MovementType, Status, Category, Subcategory, Transaction
from .serializers import (
    MovementTypeSerializer, StatusSerializer,
    CategorySerializer, SubcategorySerializer,
    TransactionSerializer,
)
from .filters import TransactionFilter

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

class MovementTypeViewSet(BaseViewSet):
    queryset = MovementType.objects.all().order_by('id')
    serializer_class = MovementTypeSerializer

    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        qs = Category.objects.filter(type_id=pk).order_by('name')
        return Response(CategorySerializer(qs, many=True).data)

class StatusViewSet(BaseViewSet):
    queryset = Status.objects.all().order_by('id')
    serializer_class = StatusSerializer

class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.select_related('type').all().order_by('id')
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        qs = Subcategory.objects.filter(category_id=pk).order_by('name')
        return Response(SubcategorySerializer(qs, many=True).data)

class SubcategoryViewSet(BaseViewSet):
    queryset = Subcategory.objects.select_related('category', 'category__type').all().order_by('id')
    serializer_class = SubcategorySerializer

class TransactionViewSet(BaseViewSet):
    queryset = (
        Transaction.objects
        .select_related('status', 'type', 'category', 'subcategory')
        .all()
    )
    serializer_class = TransactionSerializer

    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = TransactionFilter
    search_fields = ['comment']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']
