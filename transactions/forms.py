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