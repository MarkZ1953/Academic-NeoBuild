from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterViewSet
from django.urls import path


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterViewSet.as_view({ 'post': 'create' }), name='auth_register'),
]
