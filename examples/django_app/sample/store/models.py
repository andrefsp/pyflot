from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    ""
    title = models.CharField(max_lenght=128)

class Partner(models.Model):
    ""
    name = models.CharField(max_lenght=128)

class StockRecord(model.Model):
    ""
    product = models.ForeignKey(Product)
    partner = models.ForeignKey(Partner)
    number_in_stock = models.IntegerField()


class StockCount(self):
    ""
    total = models.IntegerField()
    product = models.ForeignKey(Product)
    date = models.DatetimeField()
