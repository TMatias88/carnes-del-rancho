from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_fix_image_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_file',
            field=models.ImageField(
                verbose_name='Imagen local (solo desarrollo)',
                upload_to='products/',
                blank=True,
                null=True,
            ),
        ),
    ]
