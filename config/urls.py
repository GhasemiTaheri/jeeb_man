from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('profiles.routers')),
    path('api/settings/', include('settings.routers')),
    path('api/management/', include('management.routers')),
]
