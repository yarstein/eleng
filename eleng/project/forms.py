from django import forms
from captcha.fields import CaptchaField

from .models import Resume, Feedback


class ResumeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ResumeForm, self).__init__(*args, **kwargs)

        # Если пользователь авторизован, убираем поле капчи
        if self.request and self.request.user.is_authenticated:
            if 'captcha' in self.fields:
                del self.fields['captcha']

    captcha = CaptchaField()

    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'resume_file', 'captcha']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Введите вашу фамилию'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+998(XX) XXX XX XX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите вашу электронную почту'}),
            'resume_file': forms.FileInput(),
        }


class FeedbackForm(forms.ModelForm):
    """
    Форма отправки обратной связи
    """
    captcha = CaptchaField()

    class Meta:
        model = Feedback
        fields = ('subject', 'email', 'content')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Тема письма'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите вашу электронную почту'}),
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Содержимое письма'}),
        }
