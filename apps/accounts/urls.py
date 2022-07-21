from django.conf import settings
from django.urls import include, path
from apps.accounts import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]


if settings.DEBUG:
    urlpatterns += [
        path('auth/', include('rest_framework.urls')),
    ]
