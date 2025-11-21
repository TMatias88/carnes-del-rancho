from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_product_image_product_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(
                max_length=500,
                null=True,
                blank=True,
                verbose_name='URL de imagen RAW (GitHub u otra)'
            ),
        ),
    ]
