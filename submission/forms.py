# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.forms import UserCreationForm


class SubmissionForm(UserCreationForm):
    """
    A form that creates user, with privileges to edit developer page created for given developer user
    """

    # TODO add developer name -> developer page title
    # TODO validate developer name/page title is unique

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', )

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        # require email field
        self.fields['email'].required = True
        # TODO email verification?
        # TODO force unique email per user?

    def save(self, commit=True):
        user = super(SubmissionForm, self).save(commit)
        # TODO create developer page for given user
        # TODO create permission group for given developer page
        # TODO grant created permission group to created user
        return user
