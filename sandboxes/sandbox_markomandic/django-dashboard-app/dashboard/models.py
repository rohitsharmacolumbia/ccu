from django.db import models


class Order(models.Model):
    product_category = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    shipping_cost = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

class Day(models.Model):
    currently_in_ccu = models.IntegerField()
    current_average_age = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
