# Generated by Django 3.2.5 on 2022-07-13 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specificationoption',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='spuspecification',
            name='spu',
        ),
        migrations.DeleteModel(
            name='SKUSpecification',
        ),
        migrations.DeleteModel(
            name='SpecificationOption',
        ),
        migrations.DeleteModel(
            name='SPUSpecification',
        ),
    ]
