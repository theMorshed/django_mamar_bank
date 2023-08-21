from django import forms
from transactions.models import UserTransaction

class UserTransactionForm(forms.ModelForm):
    class Meta:
        model = UserTransaction
        fields = [
            'amount',
            'transaction_type'
        ]
        
        def __init__(self, *args, **kwargs):
            self.account = kwargs.pop('account')
            super().__init__(*args, **kwargs)
            self.fields['transaction_type'].disabled = True
            self.fields['transaction_type'].widget = forms.HiddenInput()
            
        def save(self, commit=True):
            self.instance.account = self.account
            self.instance.balance_after_transaction = self.account.balance
            return super().save()
        
class UserDepositForm(UserTransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You have to deposit at least {min_deposit_amount} taka')
        return amount
    
class UserWithdrawForm(UserTransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(f'You can withdraw at least {min_withdraw_amount} taka')
        if amount > max_withdraw_amount:
            raise forms.ValidationError(f'You can\'t withdraw more than {max_withdraw_amount} taka')
        if amount > balance:
            raise forms.ValidationError(f'You don\'t have enough money to withdraw. You have only {balance} taka in your account')
        
        return amount
    
class UserLoanRequestForm(UserTransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        return amount