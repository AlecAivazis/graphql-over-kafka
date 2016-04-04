# local imports
from nautilus.models import BaseModel
from ..fields import PasswordField

class HasPassword(BaseModel):
    password = PasswordField()
