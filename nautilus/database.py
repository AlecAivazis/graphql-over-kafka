# external imports
from peewee import Proxy

# create a placeholder database
db = Proxy()

def init_db(database_url):
    """
        This function initializes the global database to point to the given url
        and associated parameters.
    """
    # utility function to parse database urls
    from playhouse.db_url import connect
    # initialize the peewee database with the appropriate engine
    db.initialize(connect(database_url))
