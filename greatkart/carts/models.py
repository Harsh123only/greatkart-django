from django.db import models
from django.db.models import ForeignKey


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
            return self.cart_id
    
    
class CartItem(models.Model):
    user= ForeignKey('accounts.Account', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    variation = models.ManyToManyField('store.Variation', blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
    

    def __unicode__(self):
        return str(self.product)
    