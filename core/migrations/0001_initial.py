# -*- coding: utf-8 -*-


import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.wagtailcore.fields
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0013_update_golive_expire_help_text'),
        ('wagtailimages', '0005_make_filter_spec_unique'),
        ('taggit', '0001_initial'),
        ('wagtaildocs', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyIndex',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Companies Index Page',
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('feed_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'verbose_name': 'Home Page',
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='MenuElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_external', models.URLField(help_text=b'Set an external link if you want the link to point somewhere outside the CMS.', null=True, verbose_name=b'External link', blank=True)),
                ('link_email', models.EmailField(help_text=b'Set the recipient email address if you want the link to send an email.', max_length=75, null=True, blank=True)),
                ('link_phone', models.CharField(help_text=b'Set the number if you want the link to dial a phone number.', max_length=20, null=True, blank=True)),
                ('explicit_name', models.CharField(help_text=b'If you want a different name than the page title.', max_length=64, null=True, blank=True)),
                ('short_name', models.CharField(help_text=b'If you need a custom name for responsive devices.', max_length=32, null=True, blank=True)),
                ('css_class', models.CharField(help_text=b'Optional styling for the menu item', max_length=255, null=True, verbose_name=b'CSS Class', blank=True)),
                ('icon_class', models.CharField(help_text=b'In case you need an icon element <i> for the menu item', max_length=255, null=True, verbose_name=b'Icon Class', blank=True)),
            ],
            options={
                'verbose_name': 'Menu item',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NavigationMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('menu_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Navigation menu',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NavigationMenuMenuElement',
            fields=[
                ('menuelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.MenuElement')),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('parent', modelcluster.fields.ParentalKey(related_name='menu_items', to='core.NavigationMenu')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('core.menuelement', models.Model),
        ),
        migrations.CreateModel(
            name='PageTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubmitFormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255)),
                ('field_type', models.CharField(max_length=16, choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')])),
                ('required', models.BooleanField(default=True)),
                ('choices', models.CharField(help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', max_length=512, blank=True)),
                ('default_value', models.CharField(help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, blank=True)),
                ('help_text', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubmitFormPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Form Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='WagtailPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Content Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='WagtailCompanyPage',
            fields=[
                ('wagtailpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.WagtailPage')),
                ('company_url', models.URLField(help_text=b'The URL of your site, something like "https://www.springload.co.nz"', null=True, blank=True)),
                ('github_url', models.URLField(null=True, blank=True)),
                ('twitter_url', models.URLField(null=True, blank=True)),
                ('location', models.CharField(max_length=128, null=True, blank=True)),
                ('logo', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'verbose_name': 'Company Page',
            },
            bases=('core.wagtailpage',),
        ),
        migrations.CreateModel(
            name='WagtailSitePage',
            fields=[
                ('wagtailpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.WagtailPage')),
                ('site_url', models.URLField(help_text=b'The URL of your site, something like "https://www.springload.co.nz"', null=True)),
                ('image_desktop', models.ForeignKey(help_text=b'Use a <b>ratio</b> of <i>16:13.28</i> and a <b>size</b> of at least <i>1200x996 pixels</i> for an optimal display.', related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
                ('image_phone', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
                ('image_tablet', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'verbose_name': 'Site Page',
            },
            bases=('core.wagtailpage',),
        ),
        migrations.AddField(
            model_name='wagtailpage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wagtailpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='core.PageTag', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submitformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='form_fields', to='core.SubmitFormPage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(related_name='tagged_items', to='core.WagtailPage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagetag',
            name='tag',
            field=models.ForeignKey(related_name='core_pagetag_items', to='taggit.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuelement',
            name='link_document',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', help_text=b'Choose an existing document if you want the link to open a document.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuelement',
            name='link_page',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailcore.Page', help_text=b'Choose an existing page if you want the link to point somewhere inside the CMS.', null=True),
            preserve_default=True,
        ),
    ]
