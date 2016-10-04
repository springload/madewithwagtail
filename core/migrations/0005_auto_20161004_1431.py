# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def cleanup_tags(apps, schema_editor):
    Tag = apps.get_model("taggit", "Tag")
    PageTag = apps.get_model("core", "PageTag")
    tags_processed = []
    duplicated_tags_id = []
    for tag in Tag.objects.all():
        if tag.name.lower() not in tags_processed:

            tags_iexact = Tag.objects.filter(name__iexact=tag.name).order_by("id")
            first_tag = tags_iexact.first()
            tags_processed.append(tag.name.lower())

            for duplicated_tag in tags_iexact:
                if duplicated_tag != first_tag:

                    for page_tag in PageTag.objects.filter(tag=duplicated_tag):
                        pt_objects = PageTag.objects
                        if not pt_objects.filter(tag=first_tag, content_object=page_tag.content_object).exists():
                            PageTag.objects.create(tag=first_tag, content_object=page_tag.content_object)
                        pt_objects.filter(tag=duplicated_tag, content_object=page_tag.content_object).delete()
                    duplicated_tags_id.append(duplicated_tag.id)
    Tag.objects.filter(id__in=duplicated_tags_id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160511_1652'),
    ]

    operations = [
        migrations.RunPython(cleanup_tags, migrations.RunPython.noop),
    ]
