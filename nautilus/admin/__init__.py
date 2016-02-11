# third party imports
from flask.ext.admin import Admin, expose
from flask.ext.admin.contrib.sqla import ModelView as Flask_ModelView

admin = Admin(template_mode='bootstrap3')

class ModelView(Flask_ModelView):
    column_display_pk = True # shows private key

def init_service(service):
    """ create the flask admin instance """
    admin.name = service.name + ' Admin'
    admin.init_app(service.app)

def add_model(model):
    # damn circular references....
    from nautilus.db import db
    # if the model has a custom AdminView defined then use it
    view = model.getAdminView() if hasattr(model, 'getAdminView') else ModelView
    # add the model to the view using its  using model view
    admin.add_view(view(model, db.session))
