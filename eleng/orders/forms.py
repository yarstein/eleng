from ckeditor.widgets import CKEditorWidget

from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    email = forms.CharField(disabled=True, required=False, label='E-mail', widget=forms.TextInput(attrs={"class": 'form-input'}))
    first_name = forms.CharField(max_length=100, required=False, label='Имя')
    last_name = forms.CharField(max_length=100, required=False, label='Фамилия')
    
    class Meta:
        model = Order
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'city', 'comments', ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={"class": 'form-input'}),
            'last_name' : forms.TextInput(attrs={"class": 'form-input'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+998(XX) XXX XX XX'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.initial['first_name'] = user.first_name
            self.initial['last_name'] = user.last_name
            self.initial['email'] = user.email


class ResponseForm(forms.ModelForm):
    admin_response = forms.CharField(widget=CKEditorWidget(), label='Сообщение')
    
    class Meta:
        model = Order
        fields = ['admin_response']

