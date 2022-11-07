from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'balance', 'status']


admin.site.register(Customer, CustomerAdmin)
