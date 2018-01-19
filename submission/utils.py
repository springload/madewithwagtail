# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.models import Group, Permission
from wagtail.wagtailcore.models import Collection, GroupCollectionPermission, GroupPagePermission

from core.models import CompanyIndex, WagtailCompanyPage


def get_developers_index_page():
    """
    Get developer company index page
    :return:
    """
    return CompanyIndex.objects.get(slug='developers', live=True)  # hardcoded way to get developers index page


def create_company_page(company_index, title, **kwargs):
    """
    Create a new company page
    """
    company_page = WagtailCompanyPage(title=title, **kwargs)
    company_index.add_child(instance=company_page)
    return company_page


def create_collection(name):
    """
    Create wagtail collection
    code follows wagtail.wagtailadmin.views.collections.Create#save_instance
    """
    collection = Collection(name=name)
    root_collection = Collection.get_first_root_node()
    root_collection.add_child(instance=collection)
    return collection


def create_wagtail_admin_group(name):
    """
    Create a new group with access to Wagtail administration
    """
    access_admin_permission = Permission.objects.get_by_natural_key(
        codename='access_admin', app_label='wagtailadmin', model='admin'
    )
    group = Group.objects.create(name=name)
    group.permissions.add(access_admin_permission)
    return group


def grant_wagtail_page_permission(permission_name, page, group):
    """
    Grant wagtail page permission to permission group
    returns True if permission granted
    """
    perm, created = GroupPagePermission.objects.get_or_create(
        group=group,
        page=page,
        permission_type=permission_name
    )
    return bool(perm)


def grant_wagtail_collection_permission(permission, collection, group):
    """
    Grant wagtail collection permission to permission group
    returns True if permission granted
    """
    perm, created = GroupCollectionPermission.objects.get_or_create(
        group=group,
        collection=collection,
        permission=permission
    )
    return bool(perm)


def get_wagtail_image_permission(name):
    """
    Get permission instance for wagtail image model
    """
    return Permission.objects.get_by_natural_key(
        codename=name,
        app_label='wagtailimages',
        model='image'
    )
