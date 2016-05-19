def tag_function(func, tag):
    # if there are no tags already assigned to the function
    if not hasattr(func, '_tags'):
        # add the set of tags to the function
        func._tags = set()

    # add the tag to the func
    func._tags.add(tag)

    # return the func
    return func


def function_has_tag(func, tag):
    # return true if the tag is in the set
    return hasattr(func, '_tags') and tag in func._tags


async_tag = '_async'

def is_async_field(func):
    """
        Marks a resolver to run inside the ioloop.
    """
    return function_has_tag(func, async_tag)

def async_field(func):
    # return a tagged version of the function
    return tag_function(func, async_tag)