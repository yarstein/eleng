from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView



from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from .mixins import UserIsNotAuthenticated
from .utils import send_email_for_verify
from django.contrib.sites.shortcuts import get_current_site
from .tasks import send_email_for_verify_task


User = get_user_model()


class EmailVerify(View):
    """Представление, обрабатывает подтверждение e-mail"""

    def get(self, request, uidb64, token):
        # получаем нашего юзера передав уникальный идентификатор
        user = self.get_user(uidb64)

        # пользователь получен и токен у нас корректен
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
        return redirect('users:invalid_verify')
    
    @staticmethod
    def get_user(uidb64):
        """
        Эта ф-я получает из uidb64 юзера, если не найден в БД, то возвращает None
        """
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    def form_valid(self, form):
        user = form.get_user()

        # Проверяем, верифицирована ли почта у пользователя
        if not user.email_verify:
            messages.error(self.request, 'Ваша электронная почта не подтверждена. Пожалуйста, проверьте вашу почту.')
            return redirect('users:login')

        # Если почта верифицирована, продолжаем стандартный процесс входа
        return super().form_valid(form)



class RegisterUser(UserIsNotAuthenticated, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Сохранение пользователя
        user = form.save()
        
        # Отправка письма с подтверждением
        # send_email_for_verify(self.request, user)

        # ----------- версия с CELERY
        current_site = get_current_site(self.request)
        # в delay() нельзя передавать объекты
        send_email_for_verify_task.delay(current_site.domain, user.id)


        return redirect('users:confirm_email')
    

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    # перенаправления после успешного изменения данных о пользователя
    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    # Отбираем ту запись, которую будем редактировать и отображать
    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"