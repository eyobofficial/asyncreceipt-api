from django.contrib import admin

from .models import Receipt, ReceiptItem


class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 1


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('seller', 'buyer', 'total', 'date', 'owner')
    list_display_links = ('seller', 'buyer')
    search_fields = ('seller', 'buyer')
    inlines = [ReceiptItemInline]
