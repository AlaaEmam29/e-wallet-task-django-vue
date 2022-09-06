from django.contrib import admin

from transaction.admin import InlineTransaction

from .models import UserAccount

class UserAccountAdmin(admin.ModelAdmin):
    inlines = [InlineTransaction]

    list_display = ('user','account_no' ,'balance')
    ordering = ['user']
    list_filter = ['balance', 'user','is_active']
admin.site.register(UserAccount,UserAccountAdmin)