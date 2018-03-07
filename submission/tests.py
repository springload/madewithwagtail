# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from mock import Mock, call, patch
from wagtail.wagtailcore.models import Collection, GroupCollectionPermission, GroupPagePermission, Page

from core.models import CompanyIndex, WagtailCompanyPage

from .utils import (
    create_collection,
    create_company_page,
    create_company_submission,
    create_wagtail_admin_group,
    get_collection_name,
    get_developers_index_page,
    get_permission_group_name,
    get_wagtail_image_permission,
    grant_wagtail_collection_permission,
    grant_wagtail_image_permissions,
    grant_wagtail_page_permission,
    grant_wagtail_page_permissions
)


class TestGetDevelopersIndexPage(TestCase):

    def test_get_developers_index_page(self):
        # Given we mock company index queryset
        params = dict(live=True)  # hardcoded way to found developers page
        expected = Mock()
        with patch.object(CompanyIndex.objects, 'get', return_value=expected) as patched_get:
            # When getting developers company index page
            index_page = get_developers_index_page()

        # Then we should get correct company index page queryset call
        self.assertIs(index_page, expected)
        patched_get.assert_called_once_with(**params)


class TestCreateCompanyPage(TestCase):

    def test_create_company_page(self):
        # Given some company index page
        index_page = Mock()
        title = 'test page title'
        # When adding a new company page
        company_page = create_company_page(index_page, title, live=False)

        # Then a new company page should be created and added to index
        self.assertIsInstance(company_page, WagtailCompanyPage)
        self.assertEqual(company_page.title, title)
        self.assertFalse(company_page.live)
        self.assertIsNone(company_page.id)  # add_child responsible for saving (mocked in this test)
        index_page.add_child.assert_called_once_with(instance=company_page)


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


class TestGetPermissionGroupName(TestCase):

    def test_get_permission_group_name(self):
        # Given some long company name
        company_name = 'some long company name' * 5
        max_length = 80  # as per Group.name max length
        # When getting permission group name
        group_name = get_permission_group_name(company_name)
        # Then valid group name should be given
        self.assertEqual(max_length, len(group_name))


class TestGetCollectionName(TestCase):

    def test_get_collection_name(self):
        # Given some long company name
        company_name = 'some long company name' * 15
        max_length = 255  # as per Collection.name max length
        # When getting permission collection name
        collection_name = get_collection_name(company_name)
        # Then valid collection name should be given
        self.assertEqual(max_length, len(collection_name))


class PatchInUtilsMixin(object):

    utils_path = 'submission.utils'

    def path_in_utils(self, target, **kwargs):
        self.patch(self.utils_path, target, **kwargs)

    def patch(self, module, target, **kwargs):
        patcher = patch('{module}.{function}'.format(module=module, function=target), **kwargs)
        self.addCleanup(patcher.stop)
        setattr(self, '{function}_mock'.format(function=target), patcher.start())


class TestCreateCompanySubmission(PatchInUtilsMixin, TestCase):

    def setUp(self):
        self.path_in_utils('get_developers_index_page')
        self.path_in_utils('create_company_page')
        self.path_in_utils('create_collection')
        self.path_in_utils('get_permission_group_name')
        self.path_in_utils('create_wagtail_admin_group')
        self.path_in_utils('get_collection_name')
        self.path_in_utils('grant_wagtail_page_permissions')
        self.path_in_utils('grant_wagtail_image_permissions')

    def test_create_company_submission(self):
        # Given some company name
        user = Mock()
        name = 'My awesome company'

        # When creating a new company submission
        result = create_company_submission(user, name)

        # Then all automate submission functions should be called
        company_page = self.create_company_page_mock.return_value
        self.get_developers_index_page_mock.assert_called_once()
        index_page = self.get_developers_index_page_mock.return_value

        # Company page created
        self.create_company_page_mock.assert_called_once_with(index_page, name, live=False)

        # Image collection created
        self.get_collection_name_mock.assert_called_once_with(name)
        collection_name = self.get_collection_name_mock.return_value
        self.create_collection_mock.assert_called_once_with(collection_name)
        collection = self.create_collection_mock.return_value

        # Permission group created
        self.get_permission_group_name_mock.assert_called_once_with(name)
        group_name = self.get_permission_group_name_mock.return_value
        self.create_wagtail_admin_group_mock.assert_called_once_with(group_name)
        permission_group = self.create_wagtail_admin_group_mock.return_value

        # Page permissions granted
        self.grant_wagtail_page_permissions_mock(company_page, permission_group, permissions=('add', 'edit'))

        # Image permissions granted
        self.grant_wagtail_image_permissions_mock(
            collection, permission_group, permissions=('add_image', 'change_image')
        )

        # Permission group granted to user
        user.groups.add.called_once_with(permission_group)

        # Correct company page returned
        self.assertIs(result, company_page)


class TestGrantWagtailPagePermissions(PatchInUtilsMixin, TestCase):

    def setUp(self):
        self.path_in_utils('grant_wagtail_page_permission')

    def test_grant_wagtail_page_permissions(self):
        # Given some permissions to be granted
        page = Mock()
        group = Mock()
        permission_add = 'add'
        permission_edit = 'edit'

        # When granting page permissions
        grant_wagtail_page_permissions(page, group, [permission_add, permission_edit])

        # Then all permissions should be granted
        expected_calls = [call(permission_add, page, group), call(permission_edit, page, group)]
        self.assertListEqual(self.grant_wagtail_page_permission_mock.mock_calls, expected_calls)


class TestGrantWagtailImagePermissions(PatchInUtilsMixin, TestCase):

    def setUp(self):
        self.path_in_utils('get_wagtail_image_permission')
        self.path_in_utils('grant_wagtail_collection_permission')

    def test_grant_wagtail_image_permission(self):
        # Given add permission to be granted
        collection = Mock()
        group = Mock()
        permission_add = 'add'

        # When granting image permission
        grant_wagtail_image_permissions(collection, group, permissions=[permission_add])

        # Then add permission should be granted
        self.get_wagtail_image_permission_mock.assert_called_once_with(permission_add)
        permission = self.get_wagtail_image_permission_mock.return_value
        self.grant_wagtail_collection_permission_mock.assert_called_once_with(permission, collection, group)

    def test_grant_wagtail_image_permissions(self):
        # Given some permissions to be granted
        collection = Mock()
        group = Mock()
        permission_add = 'add'
        permission_edit = 'edit'
        add_permission = 'add permission instance'
        edit_permission = 'edit permission instance'
        self.get_wagtail_image_permission_mock.side_effect = [add_permission, edit_permission]

        # When granting page permissions
        grant_wagtail_image_permissions(collection, group, permissions=[permission_add, permission_edit])

        # Then all permissions should be granted
        expected_calls = [call(permission_add), call(permission_edit)]
        self.assertListEqual(self.get_wagtail_image_permission_mock.mock_calls, expected_calls)

        expected_calls = [call(add_permission, collection, group), call(edit_permission, collection, group)]
        self.assertListEqual(self.grant_wagtail_collection_permission_mock.mock_calls, expected_calls)
