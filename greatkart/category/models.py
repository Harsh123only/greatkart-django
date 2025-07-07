from django.urls import reverse
from django.db import models

# Create your models here.

class category(models.Model):
    category_name=models.CharField(max_length=50,unique=True,)
    slug=models.SlugField(max_length=100,unique=True)
    Description=models.CharField(max_length=255,blank=True)
    cat_image=models.ImageField(upload_to='photos/category/',blank=True)

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('product_by_category',args=[self.slug])

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

