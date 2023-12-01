from rest_framework.routers import SimpleRouter

from management.views import TransactionViewSet

router = SimpleRouter()
router.registry('transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls
