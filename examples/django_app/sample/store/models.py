from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    ""
    title = models.CharField(max_lenght=128)


class StockRecord(models.Model):
    ""
    product = models.ForeignKey(Product)
    total_in_stock = models.IntegerField()


class StockCount(models.Model):
    "
    How many stock do we have for each product.
    total = StockRecord.objects.get(product=product).total_in_stock
    date = datetime.datetime.now()
    "
    product = models.ForeignKey(Product)
    total = models.IntegerField()
    date = models.DatetimeField()


class ProductCount(models.Model):
    """
    How many different products exists.
    total = Product.objects.count()
    date = datetime.datetime.now()
    """
    total = models.IntegerField()
    date = models.DatetimeField()

