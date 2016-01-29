from flask_login import LoginManager

loginManager = LoginManager()

def setupAuth(service):
    loginManager.init_app(service.app)
