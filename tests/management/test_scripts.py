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
        # execute the model service creation script
        self._run_cmd("naut create model foo")

    def test_can_create_connection_service(self):
        # execute the model service creation script
        self._run_cmd("naut create connection foo:bar")


    def test_can_create_api(self):
        # execute the model service creation script
        self._run_cmd("naut create api")


    def _run_cmd(self, cmd, check_for_output=False):
        """
            This method executes the given command and only returns
            if it was successfully run.
        """
        # execute the command
        process = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
        # make sure it was successfull
        assert process.returncode == 0 , (
            "Command was not sucessfully run"
        )
        # if we need to check for output
        if check_for_output:
            # make sure its not an empty bytestring
            assert process.stdout != b'', (
                "Command did not return any output"
            )
