# Generated by Django 4.1.7 on 2023-02-24 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_useractivity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile", name="dob", field=models.DateField(),
        ),
    ]
