import unittest
from unittest.mock import MagicMock

import nautilus.models as models


class TestUtil(unittest.TestCase):
    """
        This test suite checks the behavior of the various mixins that come
        with nautilus.
    """

    def test_password_field(self):
        # create a table with a password
        class TestClass(models.Model):
            password = models.fields.PasswordField()

        # create an instance of the table with a password
        record = TestClass(password="foo")

        # make sure we cannot read the password
        assert record.password != 'foo', (
            'Password could be read from model instance.'
        )


