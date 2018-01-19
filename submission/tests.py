# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.test import TestCase
from wagtail.wagtailcore.models import Collection

from submission.utils import create_collection


class TestCreateWagtailCollection(TestCase):

    def test_collection_created(self):
        # Given unique non-existing collection
        name = 'Unique collection'
        root_collection = Collection.get_first_root_node()
        self.assertFalse(root_collection.get_children().filter(name=name).exists())

        # When attempt to create a collection
        collection = create_collection(name)

        # Then collection should be created
        self.assertIsInstance(collection, Collection)
        self.assertEqual(collection.name, name)
        root_collection.refresh_from_db()  # fetch fresh data from db
        db_collection = root_collection.get_children().get(name=name)
        # verify collection created
        self.assertIsNotNone(db_collection)
        self.assertEqual(collection, db_collection)
