from django.urls import path
from .views import GameCreationViewSet, GamePurchaseViewSet

urlpatterns = [
    path('create/', GameCreationViewSet.as_view({'post': 'create'}), name='game_creation'),
    path('buy/', GamePurchaseViewSet.as_view({'post': 'create'}), name='game_purchase'),
]
