from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from profiles.views import MeView, UserManagementViewSet, RegisterApiView

router = SimpleRouter()
router.register('management', UserManagementViewSet,
                basename='user_management')

urlpatterns = [
                  path('register/', RegisterApiView.as_view(),
                       name='register_user'),
                  path('me/', MeView.as_view(), name='me'),

                  # 3rd authentication endpoints
                  path('auth/token/', TokenObtainPairView.as_view(),
                       name='token_obtain_pair'),
                  path('auth/refresh/', TokenRefreshView.as_view(),
                       name='token_refresh'),
              ] + router.urls
