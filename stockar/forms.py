from django import forms
from django.contrib.auth.forms import UserCreationForm

from stockar.models import Account


class AccountCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom', required=True, widget=forms.TextInput(attrs={'placeholder': 'Entrer votre prénom'}))
    last_name = forms.CharField(label='Nom', required=True, widget=forms.TextInput(attrs={'placeholder': 'Entrer votre nom'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'placeholder': 'Entrer votre email'}))
    password1 = forms.CharField(label='Mot de passe', required=True, widget=forms.TextInput(attrs={'placeholder': 'Entrer votre mot de passe'}))
    password2 = forms.CharField(label='Confirmation mot de passe', required=True, widget=forms.TextInput(attrs={'placeholder': 'Confirmer votre mot de passe'}))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        account = super(AccountCreationForm, self).save(commit=False)
        account.email = self.cleaned_data['email']
        if commit:
            account.save()
        return account
