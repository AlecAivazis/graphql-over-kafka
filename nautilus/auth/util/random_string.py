# external imports
import random
import string

def random_string(length):
    """
        This function generates a crytographically secure random string of alphanumeric
        characters of the appropriate length using the system random libraries.
    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
