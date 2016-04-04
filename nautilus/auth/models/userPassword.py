# local imports
from nautilus.models import fields, BaseModel
from .mixins import HasPassword

class UserPassword(HasPassword, BaseModel):
    user = fields.CharField(unique=True) # points to a remote user entry
