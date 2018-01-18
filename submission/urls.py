# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url

from submission.views import AutomateSubmission

urlpatterns = [
    url(r'^sign-up/$', AutomateSubmission.as_view()),
]
