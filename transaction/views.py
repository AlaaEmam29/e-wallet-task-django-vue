from datetime import datetime
import decimal
from django.shortcuts import render ,get_object_or_404

from account.models import UserAccount

from django.contrib import messages

from transaction.models import  Transfer ,Transaction
from .constants import FEEZ

# Create your views here.
def transactionForm(request):
    messageL = 'success'

    if request.method == 'POST':
        sender = request.POST['sender']
        receiver = request.POST['receiver']
        amount = request.POST['amount']
        sender_acc = request.POST['sender_acc']
        receiver_acc = request.POST['receiver_acc']
        sender_user = UserAccount.objects.filter(user__username=sender, account_no=sender_acc).first()
        receiver_user = UserAccount.objects.filter(user__username=receiver, account_no=receiver_acc).first()
        owner = UserAccount.objects.filter(user__username='owner').first()
        amount = decimal.Decimal(amount) 


        if sender_user is not None and receiver_user is not None:
            if sender_user.balance > amount:

                sender_user.balance -= (amount + (amount * decimal.Decimal(FEEZ)))
                
                sender_user.save()
                receiver_user.balance += amount
                receiver_user.save()

                transfer = Transfer.objects.create(sender=sender_user, receiver=receiver_user, amount=amount , timestamp=datetime.now(),
                sender_account_no=sender_acc, receiver_account_no=receiver_acc
                )
                transfer.save()
                owner.balance += amount 
                owner.save()
                message = 'success'


                messages.success(request, "Transaction Successful")
                return render(request, "transaction/transactionForm.html" , {'messageL':messageL})
            elif sender_user.balance < amount:
                message = 'error'
                messages.info(request, f'You have {sender_user.balance} $ in your account. '
                'You can not send more than your account balance')
                return render(request, "transaction/transactionForm.html", {'message':message})
            elif sender_user.balance == amount :
                messageL = 'error'
                messages.info(request,f'you can not send your account balance you should have at least have 1$ in your account ')
                return render(request, "transaction/transactionForm.html", {'messageL':messageL})
            elif sender_user.balance == 0:
                messageL = 'error'
                messages.info(request, "You can not send money from your account because your account balance is 0")
                return render(request, "transaction/transactionForm.html", {'messageL':messageL})
            elif sender == receiver:
                messageL = 'error'
                messages.info(request, "You can not send money to your self")
                return render(request, "transaction/transactionForm.html", {'messageL':messageL})
        else:
            messageL = 'error'
            messages.info(request, "Name or Account number is incorrect , please try again")
            return render(request, "transaction/transactionForm.html", {'messageL':messageL})
    return render(request, "transaction/transactionForm.html", {'messageL':messageL})


def transactionList(request, id):
    user =  UserAccount.objects.get(user_id=id)
    show_date = True
    is_staff = user.user.is_staff
    balance = user.balance

    if is_staff == False:
        show_date = False
        transfers = Transfer.objects.filter(sender=user).order_by('-timestamp')
        return render(request, "transaction/transactionList.html", {'transfers':transfers, 'balance':balance , 'show_date':show_date})
    

    else:
        show_date = True
        transfers = Transfer.objects.all().order_by('-timestamp')
        transactions = Transaction.objects.all().order_by('-timestamp')
        return render(request, "transaction/transactionList.html", {'transactions':transactions,
       'transfers' : transfers ,  'balance':balance , 'show_date':show_date})



