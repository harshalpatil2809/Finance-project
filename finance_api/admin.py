from django.contrib import admin

from .models import FinanceRecord, UserProfile


@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_type', 'category', 'date')
    search_fields = ('category', 'description', 'user__username')
    list_filter = ('transaction_type', 'category', 'date')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
