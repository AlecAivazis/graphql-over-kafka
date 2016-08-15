# external imports
import json
# local imports
from nautilus.conventions.actions import intialize_service_action
from nautilus.api.util import generate_api_schema

async def flexible_api_handler(service, action_type, payload, props, **kwds):
    """
        This query handler builds the dynamic picture of availible services.
    """
    # if the action represents a new service
    if action_type == intialize_service_action():
        # the treat the payload like json if its a string
        model = json.loads(payload) if isinstance(payload, str) else payload

        # the list of known models
        models = service._external_service_data['models']
        # the list of known connections
        connections = service._external_service_data['connections']
        # the list of known mutations
        mutations = service._external_service_data['mutations']

        # if the model is a connection
        if 'connection' in model:
            # if we haven't seen the connection before
            if not [conn for conn in connections if conn['name'] == model['name']]:
                # add it to the list
                connections.append(model)

        # or if there are registered fields
        elif 'fields' in model and not [mod for mod in models if mod['name'] == model['name']]:
            # add it to the model list
            models.append(model)

        # the service could provide mutations as well as affect the topology
        if 'mutations' in model:
            # go over each mutation announce
            for mutation in model['mutations']:
                # if there isn't a mutation by the same name in the local cache
                if not [mut for mut in mutations if mut['name'] == mutation['name']]:
                    # add it to the local cache
                    mutations.append(mutation)

        # if there are models
        if models:
            # create a new schema corresponding to the models and connections
            service.schema = generate_api_schema(
                models=models,
                connections=connections,
                mutations=mutations,
            )
