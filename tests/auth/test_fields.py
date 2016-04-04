# external imports
import unittest
# local imports
import nautilus
import nautilus.models as models

class TestUtil(unittest.TestCase):
    """
        This test suite checks the behavior of the various mixins that come
        with nautilus.
    """

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')


    def test_password_field(self):
        # create a table with a password
        class TestPassword(models.BaseModel):
            password = nautilus.auth.PasswordField()

        # create the table
        TestPassword.create_table(True)

        # create an instance of the table with a password
        record = TestPassword(password="foo")
        # save the record to the database
        record.save()

        # retireve the record
        password = TestPassword.get(TestPassword.id == record.id).password
        # make sure there is a hash assocaited with the password
        assert hasattr(password, 'hash') , (
            "Retrieved record's password did not come with a hash"
        )
        # make sure that hash hide the password
        assert password.hash != 'foo' , (
            "Retrieved record's password is in plain sight!"
        )
        # make sure we can check for password equality
        assert password == 'foo', (
            'Password could not checked for equality.'
        )

        # remove the table from the database
        TestPassword.drop_table()
