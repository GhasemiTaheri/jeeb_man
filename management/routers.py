from rest_framework.routers import SimpleRouter

from management.views import TransactionViewSet

router = SimpleRouter()
router.register('transactions', TransactionViewSet, basename='transaction')
router.register('reports', TransactionViewSet, basename='reports')

urlpatterns = router.urls
