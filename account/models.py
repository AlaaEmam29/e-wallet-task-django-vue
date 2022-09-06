from gc import freeze
import string
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


import uuid
import random
User = get_user_model()


# Create your models here.
class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_no =models.CharField(max_length=3, null=False, blank=False , default=uuid.uuid4().hex[:3])
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.user.username) + ' account' 
    





