# external imports
import unittest
# local imports
import nautilus

class TestUtil(unittest.TestCase):

    def test_can_import_responses(self):
        from nautilus.network.http import HTTPOk

