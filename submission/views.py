# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView

from .forms import SignUpForm, SubmissionForm


class SignUpView(CreateView):
    """
    Django view to handle user sign up.
    """
    form_class = SignUpForm
    template_name = 'submission/sign_up.html'
    success_url = reverse_lazy('submission_new')  # let NewSubmissionView to drive the submission steps

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        response = super(SignUpView, self).form_valid(form)
        login(self.request, user=self.object)
        return response


class AutomateSubmissionView(LoginRequiredMixin, CreateView):
    """
    Django view to handle automate submission form page.
    """
    login_url = reverse_lazy('submission_new')  # let NewSubmissionView to drive the submission steps
    form_class = SubmissionForm
    template_name = 'submission/create_company.html'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        company_page = form.create_submission(self.user)
        return HttpResponseRedirect(self.get_page_edit_url(company_page))

    def get_page_edit_url(self, page):
        """
        Get wagtail admin page edit url
        """
        return reverse('wagtailadmin_pages:edit', args=[page.id])

    @property
    def user(self):
        return self.request.user


class NewSubmissionView(RedirectView):
    """
    Django view to redirect between each automate submission step
    Step 1 - sign up
    Step 2 - create company/developer page

    Step 1 skipped if user signed in already
    """
    permanent = False  # this view points to different pages, see set_redirect_url

    def dispatch(self, request, *args, **kwargs):
        self.set_redirect_url(request.user)
        return super(NewSubmissionView, self).dispatch(request, *args, **kwargs)

    def set_redirect_url(self, user):
        """
        Sign up a new user or continue to company/developer creation
        """
        if user.is_authenticated:
            self.pattern_name = 'submission_developer'
        else:
            self.pattern_name = 'submission_signup'
