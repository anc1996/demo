# Generated by Django 3.2.5 on 2022-07-17 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_skuspecification_specificationoption_spuspecification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='default_image_url',
            field=models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='', verbose_name='默认图片'),
        ),
    ]