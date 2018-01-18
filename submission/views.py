# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView

from submission.forms import SubmissionForm


class AutomateSubmission(CreateView):
    """
    Django view to handle automate submission form page.
    """
    form_class = SubmissionForm
    template_name = 'submission/sign-up.html'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        user, company_page = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_page_edit_url(company_page))

    def get_page_edit_url(self, page):
        """
        Get wagtail admin page edit url
        """
        return reverse('wagtailadmin_pages:edit', args=[page.id])
