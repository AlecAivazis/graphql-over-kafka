# external imports
from functools import singledispatch

@singledispatch
def summarize_service(service):
    raise ValueError("Cannot summarize {!r}".format(service))