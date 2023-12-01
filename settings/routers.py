from rest_framework.routers import SimpleRouter

from settings.views import CategoryViewSet

router = SimpleRouter()
router.register('category', CategoryViewSet, basename='category')

urlpatterns = router.urls
