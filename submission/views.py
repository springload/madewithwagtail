# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.views.generic.edit import CreateView

from submission.forms import SubmissionForm


class AutomateSubmission(CreateView):
    """
    Django view to handle automate submission form page.
    """
    form_class = SubmissionForm
    template_name = 'submission/sign-up.html'
    success_url = '/'  # TODO go to developer page created for given user
