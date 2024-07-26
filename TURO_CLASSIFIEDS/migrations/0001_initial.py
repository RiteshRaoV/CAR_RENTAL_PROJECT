# Generated by Django 4.2.14 on 2024-07-23 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TURO', '0011_vehicle_transmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ad_status', models.CharField(choices=[('sold', 'Sold'), ('pending', 'Pending'), ('for sale', 'For Sale')], max_length=20)),
                ('condition', models.CharField(choices=[('used', 'Used'), ('new', 'New')], max_length=10)),
                ('description', models.TextField(max_length=200)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='TURO.vehicle')),
            ],
        ),
    ]