from django.contrib import admin
from.models import *

class ProductAdmin(admin.ModelAdmin):
    # Các trường hiển thị trong danh sách
    list_display = ('id', 'name', 'price', 'inventory_quantity', 'purchased_quantity', 'remaining_quantity')

    # Các trường chỉ đọc trong form chỉnh sửa
    readonly_fields = ('remaining_quantity', 'purchased_quantity')

    # Dùng phương thức để hiển thị remaining_quantity
    def remaining_quantity(self, obj):
        return obj.remaining_quantity
    remaining_quantity.short_description = 'Remaining Quantity'

# Đăng ký model OrderItem với list_display
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'date_added')
# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Categorie)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Banner)
