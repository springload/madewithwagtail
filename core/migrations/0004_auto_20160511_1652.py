# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_wagtailsitepage_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyindex',
            name='show_map',
            field=models.BooleanField(default=False, help_text=b'Show map of companies around the world.'),
        ),
        migrations.AddField(
            model_name='wagtailcompanypage',
            name='coords',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wagtailcompanypage',
            name='show_map',
            field=models.BooleanField(default=True, help_text=b'Show company in the map of companies around the world.'),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='link_email',
            field=models.EmailField(help_text=b'Set the recipient email address if you want the link to send an email.', max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='choices',
            field=models.CharField(help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', max_length=512, verbose_name='choices', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='default_value',
            field=models.CharField(help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='field_type',
            field=models.CharField(max_length=16, verbose_name='field type', choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')]),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='help_text',
            field=models.CharField(max_length=255, verbose_name='help text', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='label',
            field=models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='required',
            field=models.BooleanField(default=True, verbose_name='required'),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='from_address',
            field=models.CharField(max_length=255, verbose_name='from address', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='subject', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='to_address',
            field=models.CharField(help_text='Optional - form submissions will be emailed to this address', max_length=255, verbose_name='to address', blank=True),
        ),
    ]
