# Generated by Django 4.2.14 on 2024-07-24 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TURO_CLASSIFIEDS', '0006_rename_intrestrequest_interestrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='interestrequest',
            name='request_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
