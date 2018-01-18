# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from core.models import CompanyIndex, WagtailCompanyPage


def get_developers_index_page():
    """
    Get developer company index page
    :return:
    """
    return CompanyIndex.objects.get(slug='developers', live=True)  # hardcoded way to get developers index page


def create_company_page(company_index, title,  **kwargs):
    """
    Create a new company page
    """
    company_page = WagtailCompanyPage(title=title, **kwargs)
    company_index.add_child(instance=company_page)
    return company_page
