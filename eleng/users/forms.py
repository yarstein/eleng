from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.forms import widgets


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'users/custom_clearable_file_input.html'  # Указываем кастомный шаблон


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={"class": 'form-input', 'placeholder': 'Введите логин или e-mail'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": 'form-input', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={"class": 'form-input'}))
    password1 = forms.CharField(label='Пароль',  widget=forms.PasswordInput(attrs={"class": 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля',  widget=forms.PasswordInput(attrs={"class": 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name' : 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={"class": 'form-input'}),
            'first_name': forms.TextInput(attrs={"class": 'form-input'}),
            'last_name' : forms.TextInput(attrs={"class": 'form-input'}),
        }

    # def clean_password2(self):
    #     """Валидатор совпадения введеных паролей для ф-ий представлений"""
    #     cd = self.cleaned_data
    #     if cd['password1'] != cd['password2']:
    #         raise forms.ValidationError("Пароли не совпадают!")
    #     return cd['password1']
    

    def clean_email(self):
        """Валидация на уникальность email"""
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={"class": 'form-input'}))
    email = forms.CharField(disabled=True, required=False, label='E-mail', widget=forms.TextInput(attrs={"class": 'form-input'}))


    class Meta:
        model = get_user_model()
        fields = ['avatar', 'username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={"class": 'form-input'}),
            'last_name' : forms.TextInput(attrs={"class": 'form-input'}),
            'avatar': CustomClearableFileInput(),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))