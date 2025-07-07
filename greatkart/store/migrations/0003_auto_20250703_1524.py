from django.db import migrations

def set_stock_default(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    Product.objects.filter(stock__isnull=True).update(stock=0)

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_stock'),
    ]

    operations = [
        migrations.RunPython(set_stock_default),
    ]
