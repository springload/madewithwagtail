# -*- coding: utf-8 -*-


import wagtail.core.fields
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="submitformpage",
            name="body",
            field=wagtail.core.fields.RichTextField(
                help_text=b"Edit the content you want to see before the form.",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="submitformpage",
            name="from_address",
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="submitformpage",
            name="subject",
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="submitformpage",
            name="thank_you_text",
            field=wagtail.core.fields.RichTextField(
                help_text=b"Set the message users will see after submitting the form.",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="submitformpage",
            name="to_address",
            field=models.CharField(
                help_text="Optional - form submissions will be emailed to this address",
                max_length=255,
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
