from django.db import models

# Create your models here.
class Instrument(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    
    class Meta:
        app_label = 'history'

    def __str__(self):
        return self.name


class History(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    open = models.BigIntegerField(null=False, blank=False)
    high = models.BigIntegerField(null=False, blank=False)
    low = models.BigIntegerField(null=False, blank=False)
    close = models.BigIntegerField(null=False, blank=False)

    class Meta:
        app_label = 'history'
        indexes = [
            models.Index(fields=['instrument_id']),
        ]

    def __str__(self):
        return f"Ins:{self.instrument} - date:{self.date} - open:{self.open} - high:{self.high} - low:{self.low} - close:{self.close}"
    
class RecentUpdate(models.Model):
    recent_update_date_time = models.DateTimeField(null=False, blank=False)

    class Meta:
        app_label = 'history'
    
    def __str__(self):
        return f"recent_update_date_time:{self.recent_update_date_time}"
