from django.urls import path


from . import views


app_name = 'transaction'

urlpatterns = [
    path('transactionForm/', views.transactionForm, name='transactionForm'),
    path('transactionList/<int:id>', views.transactionList, name='transactionList'),
    

]
