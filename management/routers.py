from rest_framework.routers import SimpleRouter

from management.views import TransactionViewSet

router = SimpleRouter()
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
