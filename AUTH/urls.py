# AUTH/urls.py
from django.urls import path
from .views import CustomTokenObtainPairView, register, protected_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('protected/', protected_view, name='protected_view'),
]
