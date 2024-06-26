# Generated by Django 4.1.4 on 2023-12-10 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('prior_rank', models.CharField(choices=[('상', 'High'), ('중', 'Medium'), ('하', 'Low')], default='중', max_length=2)),
            ],
        ),
    ]
