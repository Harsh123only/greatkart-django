from category.models import category
from django.db import models
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255,blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='photos/products',blank=False)
    stock=models.IntegerField(default=True)
    is_avilabel=models.BooleanField(default=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name
    
class variationManager(models.Manager):
    def colors(self):
        return super(variationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(variationManager,self).filter(variation_category='size',is_active=True)
    
    

Variation_category_choice=(
    ('color','color'),
    ('size','size'),
)
    

class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=Variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    objects=variationManager()


    def __str__(self):
        return f"{self.variation_category}: {self.variation_value}"
    def __unicode__(self):
        return self.product
    def __str__(self):
        return self.variation_value
