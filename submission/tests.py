# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from wagtail.wagtailcore.models import Collection, GroupCollectionPermission, GroupPagePermission, Page

from submission.utils import (
    create_collection,
    create_wagtail_admin_group,
    get_wagtail_image_permission,
    grant_wagtail_collection_permission,
    grant_wagtail_page_permission
)


class TestCreateWagtailCollection(TestCase):

    def test_collection_created(self):
        # Given unique non-existing collection
        name = 'Unique collection'
        root_collection = Collection.get_first_root_node()
        self.assertFalse(root_collection.get_children().filter(name=name).exists())

        # When attempt to create a collection
        collection = create_collection(name)

        # Then collection should be created
        self.assertIsInstance(collection, Collection)
        self.assertEqual(collection.name, name)
        root_collection.refresh_from_db()  # fetch fresh data from db
        db_collection = root_collection.get_children().get(name=name)
        # verify collection created
        self.assertIsNotNone(db_collection)
        self.assertEqual(collection, db_collection)


class TestCreateWagtailAdminGroup(TestCase):

    def test_create_wagtail_admin_group(self):
        # Given non-existing permission group
        name = 'unique-group'
        self.assertFalse(Group.objects.filter(name=name))

        # When attempt to create a permission group
        group = create_wagtail_admin_group(name)

        # Then group with one permission should be created
        self.assertTrue(Group.objects.filter(name=name).exists())
        expect = Group.objects.get(name=name)
        self.assertEqual(group, expect)
        self.assertEqual(1, group.permissions.all().count())
        self.assertEqual('Can access Wagtail admin', group.permissions.first().name)


class TestGrantWagtailPagePermission(TestCase):

    def test_grant_wagtail_page_permission(self):
        # Given some permission group
        group = Group.objects.create(name='test group')
        page = Page.objects.create(title='test page', path='0000', depth=0)
        permission = 'add'

        # When attempt to grant permission
        granted = grant_wagtail_page_permission(permission, page, group)

        # Then we expect permission have been granted
        self.assertTrue(granted)
        self.assertTrue(GroupPagePermission.objects.filter(page=page, group=group, permission_type=permission).exists())


class TestGrantWagtailCollectionPermission(TestCase):

    def test_grant_wagtail_collection_permission(self):
        # Given some permission group
        group = Group.objects.create(name='test group')
        collection = Collection.objects.create(name='test collection', path='0000', depth=0)
        permission = Permission.objects.get_by_natural_key(
            codename='add_image', app_label='wagtailimages', model='image'
        )

        # When attempt to grant permission
        granted = grant_wagtail_collection_permission(permission, collection, group)

        # Then we expect permission have been granted
        self.assertTrue(granted)
        self.assertTrue(GroupCollectionPermission.objects.filter(collection=collection,
                                                                 group=group,
                                                                 permission=permission).exists())


class TestGetWagtailImagePermission(TestCase):

    def test_get_wagtail_image_permission(self):
        # Given standard django installation
        image_type = ContentType.objects.get(app_label='wagtailimages', model='image')
        # When get add permission
        permission = get_wagtail_image_permission('add_image')

        # Then add permission for image model expected
        self.assertIsInstance(permission, Permission)
        self.assertEqual(permission.codename, 'add_image')
        self.assertEqual(permission.content_type, image_type)
