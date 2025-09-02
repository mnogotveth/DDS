from rest_framework.routers import DefaultRouter
from .views import (
    MovementTypeViewSet, StatusViewSet,
    CategoryViewSet, SubcategoryViewSet,
    TransactionViewSet,
)

router = DefaultRouter()
router.register('types', MovementTypeViewSet, basename='type')
router.register('statuses', StatusViewSet, basename='status')
router.register('categories', CategoryViewSet, basename='category')
router.register('subcategories', SubcategoryViewSet, basename='subcategory')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
