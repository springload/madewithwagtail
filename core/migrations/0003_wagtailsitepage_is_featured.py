# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_auto_20150419_2004"),
    ]

    operations = [
        migrations.AddField(
            model_name="wagtailsitepage",
            name="is_featured",
            field=models.BooleanField(
                default=False,
                help_text=b"If enabled, this site will appear on top of the sites list of the homepage.",
                verbose_name=b"Featured",
            ),
            preserve_default=True,
        ),
    ]
