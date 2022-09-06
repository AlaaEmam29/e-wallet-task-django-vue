from django.contrib import admin

from transaction.models import Transaction,Transfer

# Register your models here.
from jet.admin import CompactInline

class InlineTransaction(CompactInline):
    model = Transaction
    extra = 1
    show_change_link = True
    
class TransactionAdmin(admin.ModelAdmin):

    list_display = ('account', 'amount', 'transaction_type', 'timestamp')
    ordering = ['account']
    list_filter = ['amount', 'transaction_type', 'timestamp']
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Transfer)
