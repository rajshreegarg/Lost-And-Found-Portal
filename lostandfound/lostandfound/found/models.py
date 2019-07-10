from django.db import models
from products.models import Lost_Product,ProductImage
# Create your models here.
class Found(models.Model):
    products=models.ManyToManyField(Lost_Product,blank=True)
    total=models.IntegerField(default='0')
    timestamp = models.DateTimeField(auto_now_add = True,auto_now=False)
    updated = models.DateTimeField(auto_now_add =False,auto_now=True)

    def __str__(self):
        return (self.id)
    def ordered_items(self):
        return self.products.all().order_by('product__id')
    def get_absolute_url(self):
        return reverse ("single_product",kwargs={"id":self.id})
