from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator

from eleng.celery import app



# В этом методе все параметры взяты из PasswordResetForm из под капота django.contrib.auth forms
# def send_email_for_verify(request, user):

#     # get_current_site() - функция для получения текущего сайта (домена), на котором запущено приложение Django.
#     current_site = get_current_site(request)    # получает текущий сайт (домен), с которого был сделан запрос.

#     context = {
#         "user": user,
#         "domain": current_site.domain,
#         "uid": urlsafe_base64_encode(force_bytes(user.pk)),    # для кодирования идентификатора пользователя.
#         "token": token_generator.make_token(user),             # генератор токенов для создания безопасного токена.
#     }
#     # render_to_string - передает в шаблон контекст, рендерить его и возвращает строкой
#     message = render_to_string('users/verify_email.html', context,)
    
#     # Титл, сообщение, кому
#     email = EmailMessage('Верификация email', message, to=[user.email],)
#     email.send()


# ----------- версия с CELERY

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site


def send_email_for_verify(domain, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        current_site = Site.objects.get(domain=domain)
        context = {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": token_generator.make_token(user),
        }
        message = render_to_string('users/verify_email.html', context)
        email = EmailMessage('Верификация email', message, to=[user.email])
        email.send()
        print("Email успешно отправлен на: ", user.email)
    except Exception as e:
        print(f'Ошибка отправки email: {str(e)}')