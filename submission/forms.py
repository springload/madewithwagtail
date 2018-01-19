# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from core.models import WagtailCompanyPage
from submission.utils import (
    create_collection,
    create_company_page,
    create_wagtail_admin_group,
    get_developers_index_page,
    get_wagtail_image_permission,
    grant_wagtail_collection_permission,
    grant_wagtail_page_permission
)


company_page_title_field = WagtailCompanyPage._meta.get_field('title')


class SubmissionForm(UserCreationForm):
    """
    A form that creates user, with privileges to edit developer page created for given developer user
    """
    company_name = company_page_title_field.formfield(
        label='Developer name',
        help_text="Who build the website? Provide a company name or your full name",
        required=True
    )

    def clean_company_name(self):
        """
        Enforce company name is unique
        """
        company_name = self.cleaned_data['company_name']
        if self.company_index_page.has_company(company_name):
            # TODO improve error message for end user
            raise ValidationError('Developer registered already.')

        return company_name

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', )

    def __init__(self, *args, **kwargs):
        self.company_index_page = kwargs.pop('company_index_page', None) or get_developers_index_page()
        super(SubmissionForm, self).__init__(*args, **kwargs)
        # require email field
        self.fields['email'].required = True
        # TODO email verification?
        # TODO force unique email per user?

    def save(self, commit=True):
        # create an user account
        user = super(SubmissionForm, self).save(commit)
        company_name = self.cleaned_data['company_name']
        # create draft company page for given user
        company_page = create_company_page(self.company_index_page, company_name, live=False)

        # create image gallery for given user
        image_collection = create_collection(company_name)

        # create a new permission group with 'Can access Wagtail admin' permission
        group = create_wagtail_admin_group(name=company_name)
        # grant company page add, edit permissions to permission group
        grant_wagtail_page_permission('add', company_page, group)
        grant_wagtail_page_permission('edit', company_page, group)

        # grant image gallery add, edit permissions to permission group
        add_image = get_wagtail_image_permission('add_image')
        change_image = get_wagtail_image_permission('change_image')
        grant_wagtail_collection_permission(add_image, image_collection, group)
        grant_wagtail_collection_permission(change_image, image_collection, group)

        # grant created permission group to created user
        user.groups.add(group)
        return user, company_page
