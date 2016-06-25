# external imports
from functools import singledispatch
import json
# local imports
from nautilus.services import ModelService, ConnectionService, AuthService, Service
from nautilus.conventions.api import service_node_name
from nautilus.conventions.services import auth_service_name
from nautilus.contrib.graphene_peewee import convert_peewee_field

def summarize_service(service, **extra_fields):
    """
        This function summarizes the provided service in a serializable
        way.

        Args:
            service (subclass of nautilus.Service): The classrecord of the service
            to summarize
    """
    # if summarizing a connection
    if issubclass(service, ConnectionService):
        return summarize_connection_service(service, **extra_fields)
    # if summarizing a model service
    elif issubclass(service, ModelService):
        return summarize_model_service(service, **extra_fields)
    # if summarizing an auth service
    if issubclass(service, AuthService):
        return summarize_auth_service(service, **extra_fields)
    # if summarizing a bare service
    if issubclass(service, Service):
        return summarize_bare_service(service, **extra_fields)
    # otherwise its a service we can't summarize
    raise ValueError("Cannot summarize {!r}".format(service))

def summarize_model_service(service, **extra_fields):

    # the fields for the service's model
    model_fields = {field.name: field for field in list(service.model.fields())}

    # add the model fields to the dictionary
    service_dict = dict(
        fields=[{
                'name': key,
                'type': type(convert_peewee_field(value)).__name__
                } for key, value in model_fields.items()
               ]
    )

    # add the extra fields to the dictionary
    service_dict.update(extra_fields)

    # return the string
    return summarize_bare_service(service, **service_dict)


def summarize_connection_service(service, **extra_fields):
    # start with the default summary
    summary = {
        'name': service_node_name(service),
        'connection': {
            'from': {
                'service': service_node_name(service.from_service),
            },
            'to': {
                'service': service_node_name(service.to_service),
            }
        }
    }

    # return the summary
    return summarize_bare_service(service, **summary)


def summarize_auth_service(service, **extra_fields):
    # return the summary like usual
    return summarize_bare_service (service, **extra_fields)


def summarize_bare_service(service, **extra_fields):
    summary =  {
        'name': service.name
    }
    # add extra fields to the summary
    summary.update(extra_fields)

    # return the summary
    return summary