# local imports
import nautilus
from nautilus.network.events import crud_handler, combine_action_handlers
from nautilus.conventions.services import model_service_name
from nautilus.network.events.actionHandlers import noop_handler
from nautilus.network.events.consumers import ActionHandler
from nautilus.contrib.graphene_peewee import convert_peewee_field
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

        Example:

            .. code-block:: python

                import nautilus
                import nautilus.models as models

                class Model(models.BaseModel):
                    name = models.fields.CharField()

                class ServiceConfig:
                    database_url = 'sqlite:////tmp/models.db'

                class MyModelService(nautilus.ModelService):
                    model = Model
                    config = ServiceConfig

    """



    model = None

    def __new__(cls, *args, **kwds):
        # make sure the service has the right name
        cls.name = model_service_name(cls.model) if cls.model else ''
        # bubble up
        return super().__new__(cls, *args)


    def __init__(self, model=None, **kwargs):
        # avoid circular depdencies
        from ..api.util import create_model_schema

        # if we were given a model for the service
        if model:
            # use the given model
            self.model = model

        # if there is no model associated with this service
        if not self.model:
            # yell loudly
            raise ValueError("Please provide a model for the model service.")

        # pull the name of the service from kwargs if it was given
        name = kwargs.pop('name', None) or model_service_name(self.model)

        # create the service
        super().__init__(
            schema=create_model_schema(self.model),
            name=name,
            **kwargs
        )
        # initialize the database
        self.init_db()


    @property
    def action_handler(self):
        # create a crud handler for the model
        model_handler = crud_handler(self.model, name=self.name)

        class ModelActionHandler(super().action_handler):

            loop = self.loop

            async def handle_action(inner_self, action_type, payload, props, **kwds):
                """
                    The default action handler for a model service call
                """
                # bubble up
                response = await super(ModelActionHandler, inner_self).handle_action(action_type=action_type, payload=payload, props=props,**kwds)
                # call the crud handler
                await model_handler(self, action_type=action_type, payload=payload, props=props,**kwds)

        return ModelActionHandler


    def init_db(self):
        """
            This function configures the database used for models to make
            the configuration parameters.
        """
        # get the database url from the configuration
        db_url = self.config.get('database_url', 'sqlite:///nautilus.db')
        # configure the nautilus database to the url
        nautilus.database.init_db(db_url)


    def summarize(self, **extra_fields):
        # the fields for the service's model
        model_fields = {field.name: field for field in list(self.model.fields())} \
                            if self.model \
                            else {}

        # add the model fields to the dictionary
        return dict(
            **super().summarize(),
            fields=[{
                    'name': key,
                    'type': type(convert_peewee_field(value)).__name__
                    } for key, value in model_fields.items()
                   ],
            **extra_fields
        )



    def get_models(self):
        """
            Returns the models managed by this service.

            Returns:
                (list): the models managed by the service
        """
        return [self.model]
