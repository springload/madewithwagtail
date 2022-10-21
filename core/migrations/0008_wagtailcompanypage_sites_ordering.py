# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_auto_20170503_2308"),
    ]

    operations = [
        migrations.AddField(
            model_name="wagtailcompanypage",
            name="sites_ordering",
            field=models.CharField(
                default=b"created",
                max_length=20,
                choices=[
                    (b"alphabetical", b"Alphabetical"),
                    (b"created", b"Created"),
                    (b"path", b"Path (i.e. manual)"),
                ],
                help_text=b"The order the sites will be listed on the page",
            ),
        ),
    ]
