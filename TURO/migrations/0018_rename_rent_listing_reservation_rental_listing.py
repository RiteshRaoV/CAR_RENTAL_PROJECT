# Generated by Django 4.2.14 on 2024-07-26 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TURO', '0017_remove_reservation_vehicle_remove_vehicle_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='rent_listing',
            new_name='rental_listing',
        ),
    ]
