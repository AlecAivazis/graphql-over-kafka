# local imports
import nautilus.models as models
from ..fields import PasswordField

class HasPassword(models.Model):
    password = PasswordField()
