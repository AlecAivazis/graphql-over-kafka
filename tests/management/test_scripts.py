# external imports
import unittest
import os
import subprocess
import tempfile
import shutil

# local imports
from tests.util.mock import Mock

class TestUtil(unittest.TestCase):

    def setUp(self):
        # make a temporary directory
        self.tempdir = tempfile.mkdtemp()
        # save the current working directory
        self.cwd = os.getcwd()
        # change the current working directory to the temporary directory
        os.chdir(self.tempdir)


    def tearDown(self):
        # change the cwd back
        os.chdir(self.cwd)
        # remove the temporary directory
        shutil.rmtree(self.tempdir)


    def test_can_create_model_service(self):
        # import the model service creation script
        from nautilus.management.scripts.create import model
        # create a model
        model.callback('foo')

    def test_can_create_connection_service(self):
        # import the model service creation script
        from nautilus.management.scripts.create import connection
        # create a model
        connection.callback(['foo:bar'])


    def test_can_create_api(self):
        # import the model service creation script
        from nautilus.management.scripts.create import api
        # create a model
        api.callback()
