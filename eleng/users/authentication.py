from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model



class EmailAuthBackend(BaseBackend):
    """
    Аутенцификация пользователей через E-mail
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()   # ссылка на модель текущего пользователя

        try:
            # получаем самого пользователя по email
            user = user_model.objects.get(email=username)
            # если пароли совпадают, возвращаем пользователя. Ф-я check_password - проверяет на корректность пароля
            if user.check_password(password):
                return user
            return None
        # исключения: такого email - не существует или возвращение несколько пользователей с одинаковыми email
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None
    
    # получаем нашего пользовател через user_id
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
        
# После требуется зарегистрировать наш кастомный EmailAuthBackend в settings.py AUTHENTICATION_BACKENDS