from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):
    # Регулярное выражение, позволяющее номер с пробелами, скобками, и без них
    phone_regex = re.compile(r'^\+998\s?(\(\d{2}\)|\d{2})\s?\d{3}\s?\d{2}\s?\d{2}$')
    
    if not phone_regex.match(value):
        raise ValidationError("Неверный формат номера телефона. Формат должен быть: '+998(XX) XXX XX XX'.")


def get_client_ip(request):
    """
    Get user's IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip