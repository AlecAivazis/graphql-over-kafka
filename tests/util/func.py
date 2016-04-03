# external imports
from unittest.mock import call

def assert_called_once_with(mock, *args, **kwds):
    spy_name = kwds.get('spy_name', 'Spy')
    # make sure the spy is called once
    assert len(mock.call_args_list) == 1, (
        spy_name + " was called an incorrect number of times."
    )
    assert mock.call_args_list[0] == call(*args), (
        spy_name + " was not called with the correct arguments."
    )
