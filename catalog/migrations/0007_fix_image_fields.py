from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_remove_category_catalog_cat_name_39f70b_idx_and_more'),
    ]

    operations = [
        # Forzamos que Django considere aplicados los cambios
        # y no intente buscar image_file nunca más.
        migrations.RunSQL(sql="", reverse_sql=""),
    ]
