from django.core.mail import EmailMessage


def mail_all(subject, message, model):
    all_users = [i.email for i in model.objects.all() if i.email != '']
    e_mail = EmailMessage(
        subject, message, to=all_users
    )
    e_mail.send()
