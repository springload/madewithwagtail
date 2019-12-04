# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20161004_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitformfield',
            name='choices',
            field=models.TextField(help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='to_address',
            field=models.CharField(help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address', blank=True),
        ),
        migrations.AlterField(
            model_name='wagtailcompanypage',
            name='company_url',
            field=models.URLField(help_text=b'The URL of your site, something like "https://www.springload.co.nz"', null=True, blank=True),
        ),
    ]
