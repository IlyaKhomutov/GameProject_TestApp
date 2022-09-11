from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('game/', include('games.urls')),
    path('', include('rest_framework.urls')),
]
