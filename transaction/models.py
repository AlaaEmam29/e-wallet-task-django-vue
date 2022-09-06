from decimal import Decimal
from django.db import models
from django.contrib import messages

from account.models import UserAccount
from transaction.constants import FEEZ, TRANSACTION_TYPE_CHOICES

import decimal

# Create your models here.
class Transaction(models.Model):


    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.transaction_type == 1:
            return f'{self.account.user} chase in {self.amount} $'
        elif self.transaction_type == 2:
            return f'{self.account.user} chase out {self.amount} $'
        
    def save(self, *args, **kwargs):
        self.amount = decimal.Decimal(self.amount)
        if self.transaction_type == 1:            
            min_chase_in_amount = 1

            
            if self.amount < min_chase_in_amount:
                raise ValueError( f'Minimum chase in amount is {min_chase_in_amount} $')
            else: 
                self.account.balance += (self.amount - self.amount * decimal.Decimal(FEEZ))
                self.account.save()
                self.account.user.save()

        elif self.transaction_type == 2:
            balance = self.account.balance
            min_chase_out_amount = 1
            max_chase_out_amount = balance - 1;
            if self.amount < min_chase_out_amount:
                raise ValueError( f'Minimum chase out amount is {min_chase_out_amount} $')
            elif self.amount > max_chase_out_amount:
                raise ValueError(f'You can not chase out more than {max_chase_out_amount} $')
            elif self.amount > balance:
                raise ValueError(
                    f'You have {balance} $ in your account. '
                    'You can not chase out more than your account balance'
                )
            else: 
                self.account.balance -= (self.amount + self.amount * decimal.Decimal(FEEZ))
                self.account.save()
                self.account.user.save()

        super().save(*args, **kwargs)


class Transfer(models.Model):
    sender =  models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='sender'
    )
    receiver = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='receiver'
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    
    sender_account_no = models.CharField(max_length=3 , blank=False , null=False ,default='000')
    receiver_account_no = models.CharField(max_length=3 , blank=False , null=False ,default='001')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.sender.user} send {self.amount} $ to {self.receiver.user}'
        