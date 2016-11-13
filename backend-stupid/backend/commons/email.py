"""Send email method."""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
import uuid


def send_email(user, token, subject, content):
    """Sending email with subject, recieption and email content."""
    template = get_template('comfirm.html')
    confirmlink = "http://cubik.vn/confirmemail/" + str(token) + "/" + str(uuid.uuid4())
    context = {'email': user.email, 'confirmlink': confirmlink}
    html_message = template.render(context)

    send_mail(
        subject,
        content,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message=html_message)


def send_email_reset_password(user, token, subject, content):
    """Sending email with subject, recieption and email content."""
    template = get_template('email_reset.html')
    reset_pass_link = "http://cubik.vn/reset_password/" + str(token)
    context = {'user_name': user.first_name, 'reset_link': reset_pass_link}
    html_message = template.render(context)

    send_mail(
        subject,
        content,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message=html_message)


def send_email_make_review(sender, recipient, subject, content, api_key):
    """Sending email with subject, recieption and email content."""
    template = get_template('make_review.html')
    make_review_link = "http://cubik.vn/make_review/sender=" + sender.email + "/" + str(api_key.key)
    list_recipient = recipient.split(', ')
    context = {'name': sender.first_name, 'make_review_link': make_review_link, 'content': content}
    html_message = template.render(context)

    send_mail(
        subject,
        content,
        settings.EMAIL_HOST_USER,
        list_recipient,
        fail_silently=False,
        html_message=html_message)
