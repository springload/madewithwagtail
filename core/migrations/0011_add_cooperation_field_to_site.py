# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-04 09:19


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_wagtailsitepage_screenshot"),
    ]

    operations = [
        migrations.AddField(
            model_name="wagtailsitepage",
            name="in_cooperation_with",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="core.WagtailCompanyPage",
            ),
        ),
    ]
