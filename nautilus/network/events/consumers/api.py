# external imports
import json
# local imports
from nautilus.api.util import generate_api_schema
from .actions import ActionHandler

class APIActionHandler(ActionHandler):
    """
        This action handler is used by the api service to build a schema
        of the underlying services as they announce their existence over
        the action system.
    """

    _models = []
    _connections = []
    _mutations = []

    consumer_pattern = '(.*\..*\.(?!(pending)))|init'

    async def handle_action(self, action_type, payload, props, **kwds):
        # the treat the payload like json if its a string
        model = json.loads(payload) if isinstance(payload, str) else payload

        # if the model is a connection
        if 'connection' in model:
            # if we haven't seen the connection before
            if not [conn for conn in self._connections if conn['name'] == model['name']]:
                # add it to the list
                self._connections.append(model)

        # or if there are registered fields
        elif 'fields' in model and not [mod for mod in self._models if mod['name'] == model['name']]:
            # add it to the model list
            self._models.append(model)

        # the service could provide mutations as well as affect the topology
        if 'mutations' in model:
            # go over each mutation announce
            for mutation in model['mutations']:
                # if there isn't a mutation by the same name in the local cache
                if not [mut for mut in self._mutations if mut['name'] == mutation['name']]:
                    # add it to the local cache
                    self._mutations.append(mutation)

        # if there are models
        if self._models:
            # create a new schema corresponding to the models and connections
            self.service.schema = generate_api_schema(
                models=self._models,
                connections=self._connections,
                mutations=self._mutations,
            )
            self.service._external_service_data = {
                'models': self._models,
                'connections': self._connections,
                'mutations': self._mutations
            }
