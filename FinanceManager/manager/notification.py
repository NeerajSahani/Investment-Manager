import datetime

from . import models, email


def investment_end():
    for investment in models.Investment.objects.filter(
            end_date__lte=datetime.date.today() + datetime.timedelta(days=4)):
        if investment.is_active:
            remain = investment.end_date - datetime.date.today()
            to = investment.user.email
            message = 'Hurry! Your investment in ' + investment.company.name + ' is about to end in ' + str(
                remain.days) + ' days\nBetter to withdraw you investment before ' + str(investment.end_date)
            email.send_email(to, 'Investment date in about to end', message)
