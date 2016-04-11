# local imports
import nautilus
from nautilus.network.amqp import crud_handler, combine_action_handlers
from nautilus.api import create_model_schema
from nautilus.conventions.services import model_service_name
from nautilus.network.amqp.actionHandlers import noop_handler
from .service import Service

class ModelService(Service):
    """
        This service acts as the primary data store in your cloud. It manages
        the records of a single model by listening for actions that indicate
        a record mutation as well as emitting actions when the mutations have
        finished (whether successfully or not). The external API is
        automatically generated to match the given model.

        Args:
            model (nautilus.BaseModel): The nautilus model to manage.
            additonal_action_handler (optional, function): An action handler
                to be called alongside the internal ones.

        Example:

            .. code-block:: python

                import nautilus
                import nautilus.models as models

                class Model(models.BaseModel):
                    name = models.fields.CharField()

                class ServiceConfig:
                    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/models.db'

                class MyModelService(nautilus.ModelService):
                    model = Model
                    config = ServiceConfig

    """

    model = None
    additional_action_handler = noop_handler

    def __init__(self, model=None, **kwargs):
        # if we were given a model for the service
        if model:
            # use the given model
            self.model = model

        # if there is no model associated with this service
        if not self.model:
            # yell loudly
            raise ValueError("Please provide a model for the model service.")

        # the schema to add to the service
        self.api_schema = create_model_schema(self.model)

        # # the action handler is a combination
        action_handler = combine_action_handlers(
            # of the given one
            self.additional_action_handler,
            # and a crud handler
            crud_handler(self.model)
        )

        # pull the name of the service from kwargs if it was given
        name = kwargs.pop('name', None) or model_service_name(self.model)

        # create the service
        super().__init__(
            schema=self.api_schema,
            action_handler=action_handler,
            name=name,
            **kwargs
        )

        # initialize the database
        self.init_db()


    def init_db(self):
        """
            This function configures the database used for models to make
            the configuration parameters.
        """
        # get the database url from the configuration
        db_url = self.config.get('database_url', 'sqlite:///nautilus.db')
        # configure the nautilus database to the url
        nautilus.database.init_db(db_url)


    def get_models(self):
        """
            Returns the models managed by this service.

            Returns:
                (list): the models managed by the service
        """
        return [self.model]
