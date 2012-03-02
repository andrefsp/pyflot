import flot
from sample.store.models import ProductCount

class ProductCount(flot.Series):
    ""
    total = flot.YVariable()
    date = flot.TimeXVariable()
    data = ProductCount.objects.all()

    class Meta:
        label = 'Total Products'


class ProductStockCount(flot.Series):
    ""
    total = flot.YVariable()
    date = flot.TimeXVariable()

    class Meta:
        label = 'Number in Stock for product'
