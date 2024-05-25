from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')

# Alternatively, you can register the model using the admin.site.register method:
# admin.site.register(Order, OrderAdmin)
