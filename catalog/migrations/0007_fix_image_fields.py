from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_remove_category_catalog_cat_name_39f70b_idx_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE catalog_product DROP COLUMN IF EXISTS image_file;",
            reverse_sql="",
        ),
    ]
