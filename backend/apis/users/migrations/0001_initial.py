# Generated by Django 5.1.1 on 2024-10-19 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("uid", models.AutoField(primary_key=True, serialize=False)),
                ("user_class", models.CharField(max_length=50)),
                ("studentid", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=50)),
                ("teamname", models.CharField(max_length=50)),
                ("pwd", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=15)),
                ("group", models.IntegerField()),
                ("number", models.IntegerField()),
            ],
        ),
    ]
