# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from core.models import WagtailCompanyPage
from submission.utils import create_company_page, get_developers_index_page

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

        # create draft company page for given developer (user)
        company_page = create_company_page(self.company_index_page, self.cleaned_data['company_name'], live=False)

        # TODO create permission group for given developer page
        # TODO grant created permission group to created user
        return user, company_page
