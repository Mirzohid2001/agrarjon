from django.contrib import admin

from finance.models import Transaction
from blog.models import Order
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.urls import path
from django.utils.html import format_html


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ('order', 'amount', 'type', 'description')
    list_display = ["amount", "state", "type"]
    list_display_links = ["amount", "type"]
    list_editable = ("state",)


@admin.action(description=_('Показать активные заказы'))
def show_active_orders(modeladmin, request, queryset):
    modeladmin.is_archived_filter = False
    return modeladmin.changelist_view(request)


@admin.action(description=_('Показать архивированные заказы'))
def show_archived_orders(modeladmin, request, queryset):
    modeladmin.is_archived_filter = True
    return modeladmin.changelist_view(request)
