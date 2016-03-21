# local imports
from nautilus.network import CRUDHandler, combine_action_handlers
from nautilus.api import create_model_schema
from nautilus.conventions.services import model_service_name
from nautilus.network.actionHandlers import noop_handler
from nautilus.admin import add_model as add_model_to_admin
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
                from sqlalchemy import Column, Text
                from nautilus.models import HasID, BaseModel, CRUDNotificationCreator


                # these mixins provide make the model "live". For more information,
                # see foo_bar.
                class Model(CRUDNotificationCreator, HasID, BaseModel):
                    name = Column(Text)


                class ServiceConfig:
                    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/models.db'


                service = ModelService(
                    model = Model,
                    configObject = ServiceConfig,
                )

    """

    def __init__(self, model, additonal_action_handler = noop_handler, **kwargs):
        # save a reference to the model this service is managing
        self.model = model

        # the schema to add to the service
        schema = create_model_schema(model)

        # # the action handler is a combination
        # action_handler = combine_action_handlers(
        #     # of the given one
        #     additonal_action_handler,
        #     # and a crud handler
        #     CRUDHandler(model)
        # )

        # pull the name of the service from kwargs if it was given
        name = kwargs.pop('name', None) or model_service_name(model)

        # create the service
        super().__init__(
            schema=schema,
            # action_handler=action_handler,
            name=name,
            **kwargs
        )

    # def run(self, **kwargs):

    #     # register the class with the admin interface
    #     add_model_to_admin(self.model)


    #     super().run(**kwargs)
