# external imports
import unittest
import os
import tempfile
# local imports
from tests.util.mock import Mock

class TestUtil(unittest.TestCase):

    def test_render_template(self):
        # import the render utility
        from nautilus.management.util import render_template

        # the path for the mock template
        mock_template = os.path.join(
            os.path.dirname(__file__),
            'mock_template'
        )

        # open a temporary directory to render to template in
        with tempfile.TemporaryDirectory() as temp_dir:
            # render the template in the directory
            render_template(mock_template, temp_dir, {
                'name': 'mock'
            })
            # walk the temporary directory
            for dirName, subdirList, fileList in os.walk(temp_dir):
                # if we're looking at the temporary directory
                if dirName == temp_dir:
                    # the there should be two files
                    assert fileList == ['hello', 'mock'], (
                        "Root level dir did not have correct contents."
                    )
                    # open the file with dynamic contents
                    with open(os.path.join(temp_dir, 'hello')) as file:
                        # make sure the contents are what they should be
                        assert file.read() == 'mock', (
                            "Dyanmic contents did not have the correct value"
                        )

                # or if we're looking at the subdirectory
                elif dirName == os.path.join(temp_dir, 'subdir'): pass
                # otherwise we're looking at a dir we dont know about
                else:
                    raise ValueError("Encountered unknown directory")
