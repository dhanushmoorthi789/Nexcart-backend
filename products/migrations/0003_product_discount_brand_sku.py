import django.core.validators
from django.db import migrations, models
 
 
class Migration(migrations.Migration):
 
    dependencies = [
        ('products', '0002_initial'),
    ]
 
    operations = [
        # discount_price ─────────────────────────────────────────────────────
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(
                blank=True, null=True,
                decimal_places=2, max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
                help_text='Sale price. Leave blank for no discount.',
            ),
        ),
 
        # brand ──────────────────────────────────────────────────────────────
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
 
        # sku ────────────────────────────────────────────────────────────────
        # Step 1: add as nullable so existing rows don't violate NOT NULL
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(
                blank=True, null=True,
                max_length=100,
                help_text='Unique product / stock-keeping code.',
            ),
        ),
        # Step 2: backfill empty SKUs with a uuid-derived value
        migrations.RunSQL(
            sql=r"""
                UPDATE products_product
                SET sku = UPPER(SUBSTR(HEX(RANDOMBLOB(5)), 1, 10))
                WHERE sku IS NULL OR sku = '';
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Step 3: now enforce unique + not-null
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(
                blank=True, unique=True, max_length=100,
                help_text='Unique product / stock-keeping code.',
            ),
        ),
    ]