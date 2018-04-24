from django import forms
from .models import Menu

class OrderForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('item', 'subItem')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subItem'].queryset = Menu.objects.none()
