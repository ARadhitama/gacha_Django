from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class itemList(models.Model):
    item_name = models.CharField(max_length=20)
    chance = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    item_type = models.CharField(max_length=10)
    item_id = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.name

class itemSpinHistory(models.Model):
    item_id = models.PositiveIntegerField(default=0)
    item_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    spin_type = models.PositiveIntegerField(default=0)
    t_open_id = models.PositiveIntegerField(primary_key=False, default=0)
    