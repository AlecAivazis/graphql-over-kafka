# external imports
from functools import singledispatch
from ...services import ModelService, ConnectionService, AuthService

@singledispatch
def summarize_service(service):
    raise ValueError("Cannot summarize {!r}".format(service))

@summarize_service.register(ModelService)
def summarize_model_service(service, **extra_fields):

    # the dictionary representing the model service
    service_dict = {
        'name': service_node_name(service),
    }
    # the fields for the service's model
    model_fields = {field.name: field for field in list(service.model.fields())}

    # add the model fields to the dictionary
    service_dict['fields'] = [{
        'name': key,
        'type': type(convert_peewee_field(value)).__name__
    } for key, value in model_fields.items()]

    # add the extra fields to the dictionary
    service_dict.update(extra_fields)

    # return the string
    return json.dumps(service_dict)


@summarize_service.register(ConnectionService)
def summarize_connection_service(service):
    return 'hello'

@summarize_service.register(AuthService)
def summarize_auth_service(service):
    return 'hello'