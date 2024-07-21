# Generated by Django 5.0.7 on 2024-07-21 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TURO', '0010_vehicleimages_thumbnail_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='transmission',
            field=models.CharField(choices=[('manual', 'Manual'), ('automatic', 'Automatic')], default=None, max_length=25),
        ),
    ]