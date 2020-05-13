import datetime, pandas as pd
from django.db import models
from analyzer.base import Predict
from analyzer.models import CustomUser, Company


# Create your models here.

class Investment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=60))
    units = models.IntegerField(default=1)
    remark = models.TextField(blank=True, null=True)
    file = models.FilePathField(editable=False, blank=True)

    @property
    def is_active(self):
        return True if self.end_date >= datetime.date.today() else False

    def __str__(self):
        return str(self.user) + ' - ' + str(self.company) + ' - ' + str(self.start_date)

    def save(self, *args, **kwargs):
        if not self.id:
            model = Predict(ticker=self.company.symbol, days=(self.end_date - self.start_date).days,
                            start=self.start_date)
            predicted = model.get_plot()['data'].items()
            df = pd.DataFrame(predicted)
            df.columns = ['date', 'open']
            df.set_index('date', inplace=True)
            path = 'media/files/' + str(self.user) + '-' + str(self.company) + '-' + str(self.start_date) + '.csv'
            df.to_csv(path)
            self.file = path
        super(Investment, self).save(*args, **kwargs)

# data = models.Company.objects.get(slug=slug)
# data.views += 1
# model = Predict(ticker=data.symbol, days=days)
# context = model.get_plot()
# context['data'] = data
