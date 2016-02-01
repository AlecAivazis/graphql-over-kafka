# third party imports
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
# local imports
from . import db

admin = Admin(template_mode='bootstrap3')

def init_service(service):
    """ create the flask admin instance """
    admin.name = service.name + ' Admin'
    admin.init_app(service.app)

def add_model(model):
    """ add a model to the service's admin instance """
    admin.add_view(ModelView(model, db.session))
