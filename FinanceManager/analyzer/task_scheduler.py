from apscheduler.schedulers.background import BackgroundScheduler
from analyzer.base import update as update_period
from manager.notification import investment_end


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_period, 'interval', days=15)
    scheduler.add_job(investment_end, 'interval', days=1)
    scheduler.start()
