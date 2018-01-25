# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.models import Group, Permission
from django.utils.text import slugify
from wagtail.wagtailcore.models import Collection, GroupCollectionPermission, GroupPagePermission

from core.models import CompanyIndex, WagtailCompanyPage


def get_developers_index_page():
    """
    Get developer company index page
    :return:
    """
    return CompanyIndex.objects.get(live=True)  # hardcoded - developers index page is a singleton


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


def get_permission_group_name(company_name):
    """
    Creates permission group name based on company name
    """
    suffix = '-company-page'
    length_limit = Group._meta.get_field('name').max_length - len(suffix)
    name = slugify(company_name)[:length_limit]
    return name + suffix


def get_collection_name(company_name):
    """
    Creates wagtail collection name based on company name
    """
    suffix = '-collection'
    length_limit = Collection._meta.get_field('name').max_length - len(suffix)
    name = slugify(company_name)[:length_limit]
    return name + suffix


def create_company_submission(user, company_name, company_index_page=None):
    """
    Creates a company page and sets all necessary permissions
    """
    company_index_page = company_index_page or get_developers_index_page()
    # create draft company page
    company_page = create_company_page(company_index_page, company_name, live=False)
    # create image gallery
    image_collection = create_collection(get_collection_name(company_name))

    # create a new permission group with 'Can access Wagtail admin' permission
    group = create_wagtail_admin_group(get_permission_group_name(company_name))
    # grant company page add, edit permissions to permission group
    grant_wagtail_page_permissions(company_page, group, permissions=('add', 'edit'))
    # grant image gallery add, edit permissions to permission group
    grant_wagtail_image_permissions(image_collection, group, permissions=('add_image', 'change_image'))
    # grant created permission group to user
    user.groups.add(group)
    return company_page


def grant_wagtail_page_permissions(page, group, permissions):
    """
    Grant permissions for given wagtail page to given permission group
    """
    for permission in permissions:
        grant_wagtail_page_permission(permission, page, group)


def grant_wagtail_image_permissions(collection, group, permissions):
    """
    Grant wagtail image permissions for given wagtail collection to given permission group
    """
    for permission_name in permissions:
        permission = get_wagtail_image_permission(permission_name)
        grant_wagtail_collection_permission(permission, collection, group)
