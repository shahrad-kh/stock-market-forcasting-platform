from .models import Prediction
import logging
from django.db.utils import DatabaseError

logger = logging.getLogger(__name__)

class predictionRepository():
    @staticmethod
    def remove_prediction_less_than(date):
        try:
            deleted_count, _ = Prediction.objects.filter(date__lt=date).delete()
            logger.info(f"Deleted {deleted_count} old predictions before {date}")
        except DatabaseError as e:
            logger.error(f"Database error while deleting predictions: {e}")