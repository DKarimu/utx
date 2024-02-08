import logging

from django.db import models

logger = logging.getLogger(__name__)


class Order(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    success = models.BooleanField(default=False)  # Set an appropriate default value
    order_id = models.CharField(max_length=255, db_index=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField(max_length=50)
    time_in_force = models.CharField(max_length=50)
    stop_loss_rate = models.DecimalField(max_digits=10, decimal_places=2)
    pair = models.CharField(max_length=10, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    utx_create_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Order instance: {e}")
            pass

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting Order instance: {e}")
            pass

    class Meta:
        app_label = "data"
