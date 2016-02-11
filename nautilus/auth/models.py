# external imports
from sqlalchemy import Column, Text
# local imports
from nautilus.models import BaseModel, HasID, HasPassword

class UserPassword(BaseModel, HasID, HasPassword):
    user = Column(Text, unique=True) # points to a remote user entry
