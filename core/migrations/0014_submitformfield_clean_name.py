# Generated by Django 2.2.27 on 2022-03-21 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_auto_20211208_1153"),
    ]

    operations = [
        migrations.AddField(
            model_name="submitformfield",
            name="clean_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Safe name of the form field, the label converted to ascii_snake_case",
                max_length=255,
                verbose_name="name",
            ),
        ),
    ]
