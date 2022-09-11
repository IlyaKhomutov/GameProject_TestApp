from django.contrib import admin

from .models import CustomUser, Deposit

admin.site.register(CustomUser)
admin.site.register(Deposit)
