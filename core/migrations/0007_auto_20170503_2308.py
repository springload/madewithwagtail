# -*- coding: utf-8 -*-


import django.db.models.deletion
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_wagtail_1_6_upgrade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyindex',
            name='show_map',
            field=models.BooleanField(default=False, help_text='Show map of companies around the world.'),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='css_class',
            field=models.CharField(blank=True, verbose_name='CSS Class', help_text='Optional styling for the menu item', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='explicit_name',
            field=models.CharField(blank=True, help_text='If you want a different name than the page title.', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='icon_class',
            field=models.CharField(blank=True, verbose_name='Icon Class', help_text='In case you need an icon element <i> for the menu item', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='link_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', blank=True, help_text='Choose an existing document if you want the link to open a document.', to='wagtaildocs.Document', null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='link_email',
            field=models.EmailField(blank=True, help_text='Set the recipient email address if you want the link to send an email.', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='link_external',
            field=models.URLField(blank=True, verbose_name='External link', help_text='Set an external link if you want the link to point somewhere outside the CMS.', null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='link_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', blank=True, help_text='Choose an existing page if you want the link to point somewhere inside the CMS.', to='wagtailcore.Page', null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='link_phone',
            field=models.CharField(blank=True, help_text='Set the number if you want the link to dial a phone number.', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='short_name',
            field=models.CharField(blank=True, help_text='If you need a custom name for responsive devices.', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, help_text='Edit the content you want to see before the form.'),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='thank_you_text',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, help_text='Set the message users will see after submitting the form.'),
        ),
        migrations.AlterField(
            model_name='wagtailcompanypage',
            name='company_url',
            field=models.URLField(blank=True, help_text='The URL of your site, something like "https://www.springload.co.nz"', null=True),
        ),
        migrations.AlterField(
            model_name='wagtailcompanypage',
            name='show_map',
            field=models.BooleanField(default=True, help_text='Show company in the map of companies around the world.'),
        ),
        migrations.AlterField(
            model_name='wagtailsitepage',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='If enabled, this site will appear on top of the sites list of the homepage.', verbose_name='Featured'),
        ),
        migrations.AlterField(
            model_name='wagtailsitepage',
            name='site_url',
            field=models.URLField(blank=True, help_text='The URL of your site, something like "https://www.springload.co.nz"', null=True),
        ),
    ]
