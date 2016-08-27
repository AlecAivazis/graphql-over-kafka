# external imports
import unittest
# local imports
import nautilus.models as models
from nautilus.auth.util import (
    generate_session_token,
    read_session_token
)
from nautilus.auth.util.token_encryption_algorithm import token_encryption_algorithm

class TestUtil(unittest.TestCase):
    """
        This test suite checks the behavior of the various mixins that come
        with nautilus.
    """

    def test_has_session_encryption_algorithm(self):
        # just make sure we have a value
        assert isinstance(token_encryption_algorithm(), str), (
            "Could not retrieve session token encryption algorithm."
        )


    def test_read_write_session_token(self):
        # the secret key to use
        secret_key = 'asdf'
        # generate a session token
        session_token = generate_session_token(secret_key, user=1)
        # make sure we got a string back
        assert isinstance(session_token, str), (
            "Generated session token was not a string."
        )

        # make sure we can read it back
        assert read_session_token(secret_key, session_token) == {
            'user': 1
        }, (
            "Read session token did not match expecatations."
        )

        try:
            # make sure it would fail if we passed an invalid key
            read_session_token(secret_key, session_token)
            # if we got here then something went wrong
            raise AssertionError("Invalid key was able to read session token")
        except:
            pass