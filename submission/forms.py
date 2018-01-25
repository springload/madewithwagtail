# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction
from wagtail.wagtailcore.models import Collection

from core.models import WagtailCompanyPage
from core.utilities import has_recaptcha

from .utils import create_company_submission, get_collection_name, get_developers_index_page, get_permission_group_name

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
    if has_recaptcha():
        captcha = ReCaptchaField(label='')

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', )

    def __init__(self, *args, **kwargs):
        self.company_index_page = kwargs.pop('company_index_page', None) or get_developers_index_page()
        super(SubmissionForm, self).__init__(*args, **kwargs)
        # require email field
        self.fields['email'].required = True
        # TODO email verification?
        # TODO force unique email per user?

    def clean_company_name(self):
        """
        Enforce company name is unique
        """
        company_name = self.cleaned_data['company_name']
        group_name = get_permission_group_name(company_name)
        collection_name = get_collection_name(company_name)
        if self.company_index_page.has_company(company_name) or \
           Group.objects.filter(name__iexact=group_name).exists() or \
           Collection.get_first_root_node().get_children().filter(name__iexact=collection_name):
            # TODO improve error message for end user
            raise ValidationError('Developer registered already.')

        return company_name

    @transaction.atomic()
    def save(self, commit=True):
        # create an user account
        user = super(SubmissionForm, self).save(commit)
        company_page = create_company_submission(user, self.cleaned_data['company_name'], self.company_index_page)
        return user, company_page
