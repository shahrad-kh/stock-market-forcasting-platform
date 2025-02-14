from django.db import models
from history import models as history_models

class Prediction(models.Model):
    instrument = models.ForeignKey(history_models.Instrument, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    open = models.BigIntegerField(null=False, blank=False)
    high = models.BigIntegerField(null=False, blank=False)
    low = models.BigIntegerField(null=False, blank=False)
    close = models.BigIntegerField(null=False, blank=False)
    volume = models.BigIntegerField(null=False, blank=False)

    class Meta:
        app_label = 'forcast'

    def __str__(self):
        return f"Ins:{self.instrument} - date:{self.date} - open:{self.open} - high:{self.high} - low:{self.low} - close:{self.close} - volume:{self.volume}"
