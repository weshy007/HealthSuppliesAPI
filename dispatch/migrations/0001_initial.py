# Generated by Django 3.2.8 on 2021-10-14 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(choices=[('Storage_and_Transport_Medical_Equipment', 'Storage_and_Transport_Medical_Equipment'), ('Durable_Medical_Equipment', 'Durable_Medical_Equipment'), ('Diagnostic_Medical_Equipment', 'Diagnostic_Medical_Equipment'), ('Electronic_Medical_Equipment', 'Electronic_Medical_Equipment'), ('Surgical_Medical_Equipment', 'Surgical_Medical_Equipment'), ('Acute_Care', 'Acute_Care'), ('Procedural_Medical_Equipment', 'Procedural_Medical_Equipment'), ('Others', 'Others')], max_length=255)),
                ('item_description', models.CharField(blank=True, max_length=255)),
                ('item_quantity', models.CharField(blank=True, max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
