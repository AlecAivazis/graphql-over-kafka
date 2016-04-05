# local imports
from .base import AuthRequestHandler
from ..models import UserPassword
from .forms import RegistrationForm

class RegisterHandler(AuthRequestHandler):
    """
        This class handles the basic login form.
    """

    def get(self):
        # import the template directory
        from nautilus.auth.requestHandlers import template_dir
        # create the template loader
        template_loader = tornado.template.Loader(template_dir)
        # load the template from the file system
        template = template_loader.load('register.html')

        # create a login form to show in the view
        form = RegistrationForm()
        # write the template to the client
        return self.finish(template.generate(form=form))


    def post(self):
        # create a form from the request parameters
        form = RegistrationForm(self.arguments)

        # if we recieved a post request with valid information
        if form.validate():
            # the form data
            data = form.data

            # create an entry in the user password table
            password = UserPassword(**data)
            # save it to the database
            password.save()

            # move the user along
            return self.redirect(request.args.get('next'))


        # the username and password do not match
        raise tornado.httputil.HTTPInputError(
            "Sorry, could not register that username/password."
        )

            # otherwise the given password does not match the stored hash
            # else:
                # add an error to the form
                # flash('Sorry, that user/password combination was invalid.')
