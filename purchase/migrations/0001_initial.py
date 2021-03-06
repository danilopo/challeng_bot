# Generated by Django 3.2.9 on 2021-12-04 20:47

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
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_finish', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('value', models.FloatField()),
                ('purchase_date', models.DateField()),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Em validação'), (2, 'Aprovado')], default=1)),
                ('removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reseller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='resellers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
