import sys

from django.core.management import call_command
from django.test import Client, TestCase

FIXTURES_FILE = "core/fixtures/initial_data.json"


class WagtailTest(TestCase):
    """
    TestCase that loads a number fo fixtures before each execution.
    """

    def setUp(self):
        call_command("loaddata", FIXTURES_FILE, verbosity=1)
        self.client = Client()


def str_to_class(field):
    """
    String to class generator
    """
    try:
        identifier = getattr(sys.modules[__name__], field)
    except AttributeError:
        raise NameError("%s doesn't exist." % field)
    if isinstance(identifier, type):
        return identifier
    raise TypeError("%s is not a class." % field)
