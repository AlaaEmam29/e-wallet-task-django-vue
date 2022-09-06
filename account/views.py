from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib import auth
from django.contrib import messages
from .models import UserAccount
from django.contrib.auth.decorators import login_required

@login_required(login_url="login/")
def index(request):
    return render(request, "core/index.html")
def login(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate( username=username, password=password)
                
        # user = UserAccount.objects.filter(user__username=username , account_no = account_no).first()
        if user is not None:
            auth_login(request, user)
            if user.is_staff is True:
              return redirect("transaction:transactionList", id=user.id)
            else:
                return redirect("transaction:transactionForm")

        else:
            messages.info(request, "Name or Account number is incorrect , please try again")
            return redirect("account:login")
    return render(request, "account/login.html")

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("account:login")
