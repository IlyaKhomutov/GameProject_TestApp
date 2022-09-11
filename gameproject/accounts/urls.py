from django.urls import path
from .views import RegistrationAPIView, DepositViewSet, DepositsListViewSet, RollbackView, ProfileViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registraion'),
    path('profile/', ProfileViewSet.as_view({'get': 'retrieve'}), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('deposit/', DepositViewSet.as_view({"post": "create"}), name='deposit'),
    path('deposits/', DepositsListViewSet.as_view({'get': 'list'}), name='deposits list'),
    path('rollback/<uuid:id>/', RollbackView.as_view(), name='rollback'),
    ]
