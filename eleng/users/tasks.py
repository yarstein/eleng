from celery import shared_task

from .utils import send_email_for_verify


@shared_task
def send_email_for_verify_task(domain, user_id):
    """
    1. Задача обрабатывается в представлении: RegisterUser
    2. Отправка письма подтверждения осуществляется через функцию: send_email_for_verify
    """
    return send_email_for_verify(domain, user_id)