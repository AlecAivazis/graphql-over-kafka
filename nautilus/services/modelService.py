# local imports
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

                from nautilus import ModelService
                import nautilus.models as models

                class Model(models.BaseModel):
                    name = models.fields.CharField()

                class ServiceConfig:
                    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/models.db'

                service = ModelService(
                    model = Model,
                    config = ServiceConfig
                )

    """

    model = None
    additonal_action_handler = noop_handler
    api_schema = None

    def __init__(self, **kwargs):
        # make sure there is a model
        assert self.model, (
            "Please provide a model for the model service."
        )

        # the schema to add to the service
        self.api_schema = create_model_schema(self.model)

        # # the action handler is a combination
        action_handler = combine_action_handlers(
            # of the given one
            self.additonal_action_handler,
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

    def get_models(self):
        """
            Returns the models managed by this service.

            Returns:
                (list): the models managed by the service
        """
        return [self.model]
