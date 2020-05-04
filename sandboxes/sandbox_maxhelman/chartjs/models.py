from django.db import models

# Create your models here.
class Day(models.Model):
    currently_in_ccu = models.IntegerField()
    current_average_age = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()