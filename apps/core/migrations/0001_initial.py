# Generated by Django 4.0.6 on 2022-07-21 23:00

import django.core.serializers.json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('serial_no', models.CharField(max_length=100, unique=True)),
                ('model', models.CharField(choices=[('Lightweight', 'Lightweight'), ('Middleweight', 'Middleweight'), ('Cruiserweight', 'Cruiserweight'), ('Heavyweight', 'Heavyweight')], max_length=30)),
                ('weight_limit', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(500)])),
                ('battery', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('state', models.CharField(choices=[('IDLE', 'IDLE'), ('LOADING', 'LOADING'), ('LOADED', 'LOADED'), ('DELIVERING', 'DELIVERING'), ('DELIVERED', 'DELIVERED'), ('RETURNING', 'RETURNING')], default='IDLE', max_length=15)),
            ],
            options={
                'verbose_name': 'Drone',
                'verbose_name_plural': 'Drones',
            },
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('weight', models.PositiveSmallIntegerField()),
                ('code', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='medication/')),
            ],
            options={
                'verbose_name': 'Medication',
                'verbose_name_plural': 'Medications',
            },
        ),
        migrations.CreateModel(
            name='MedicationCharged',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivered', models.BooleanField(default=False)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medication_charged', to='core.drone')),
                ('medications', models.ManyToManyField(related_name='medication_charged', to='core.medication')),
            ],
            options={
                'verbose_name': 'Medication Charged',
                'verbose_name_plural': 'Medications Charged',
            },
        ),
        migrations.CreateModel(
            name='DroneLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('battery_history', models.JSONField(blank=True, default=list, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('drone', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='drone_log', to='core.drone')),
            ],
            options={
                'verbose_name': 'Drone Log',
                'verbose_name_plural': 'Drone Logs',
            },
        ),
    ]
