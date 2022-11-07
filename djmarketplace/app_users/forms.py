from django import forms
from django.forms import NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Customer


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=_('Name'), max_length=30, required=True, help_text=_('Enter the name'))
    last_name = forms.CharField(label=_('Surname'), max_length=30, required=True, help_text=_('Enter the surname'))
    email = forms.EmailField(label='E-mail', required=True, help_text=_('Enter your email address'))
    phone_number = forms.CharField(label=_('Phone number'), validators=[Customer.phoneNumberRegex], max_length=16,
                                   required=True, help_text=_('Enter your phone number'))
    address = forms.CharField(label=_('Address'), widget=forms.Textarea, help_text=_('Enter the address'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'password1', 'password2']


class CustomerBalanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].widget.attrs.update({'min': '1'})
        self.fields['balance'].widget.attrs.update({'max': '10000'})

    class Meta:
        model = Customer
        fields = ['balance']
        labels = {
            'balance': '',
        }
        widgets = {
            'balance': NumberInput(attrs={'class': 'balance_form', 'onchange': 'disable(this.value)'}),
        }
