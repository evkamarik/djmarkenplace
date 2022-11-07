from django import forms
from django.forms import NumberInput
from django.utils.translation import gettext_lazy as _
from .models import CartItem


class ItemCountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['count'].widget.attrs.update({'min': '1'})

    class Meta:
        model = CartItem
        fields = ['count']
        labels = {
            'count': '',
        }
        widgets = {
            'count': NumberInput(attrs={'class': 'item_count_input', 'onchange': 'disable(this.value)'}),
        }

