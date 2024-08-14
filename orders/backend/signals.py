from django.dispatch import Signal, receiver
# from .utilities import send_activation_notofication
from typing import Type
from .models import User
from django.db.models.signals import post_save
from orders.settings import ALLOWED_HOSTS
from django.core.signing import Signer
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

user_registered = Signal()
signer = Signer()


@receiver(user_registered)
def user_registered_dispatcher(user, **kwargs):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
        # host = 'smtp.mail.ru'
    # print(user)`
    # token, _ = ConfirmEmailToken.objects.get_or_create(user_id=instance.pk)
    context = {'user': user, 'host': host, 'sign': signer.sign(user.first_name)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    # user.email_user(subject, body_text)
    msg = EmailMultiAlternatives(
        # title:
        subject,
        # message:
        body_text,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()