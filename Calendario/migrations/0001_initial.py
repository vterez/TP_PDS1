# Generated by Django 3.2.5 on 2021-07-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('horario', models.DateTimeField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
