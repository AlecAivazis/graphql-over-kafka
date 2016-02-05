# external imports
from sqlalchemy import Column, Integer

class HasID(object):
    """ This mixing adds an auto-incrementing primary key called `id` """
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
