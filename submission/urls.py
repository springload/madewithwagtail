# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url

from submission.views import AutomateSubmissionView, NewSubmissionView

urlpatterns = [
    url(r'new/$', NewSubmissionView.as_view(), name='submission_new'),
    url(r'^developer/$', AutomateSubmissionView.as_view(), name='submission_developer'),
]
