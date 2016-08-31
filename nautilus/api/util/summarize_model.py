# local imports
from nautilus.contrib.graphene_peewee.converter import convert_peewee_field
from nautilus.conventions.models import get_model_string

def summarize_model(model):
    # print(model)
    return {
        'name': get_model_string(model),
        'fields': [
            {
                'name': field.name,
                'type': type(convert_peewee_field(field)).__name__ \
            } for field in model.fields()
        ]
    }