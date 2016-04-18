# external imports
from graphene.core.classtypes.objecttype import ObjectType
from graphene.core.classtypes.objecttype import ObjectTypeOptions
# local imports
from nautilus.contrib.graphene_peewee import convert_peewee_field

VALID_ATTRS = ('model',)

class PeeweeObjectTypeOptions(ObjectTypeOptions):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.valid_attrs += VALID_ATTRS
        self.model = None

    def contribute_to_class(self, cls, name):
        # bubble up the chain
        super().contribute_to_class(cls, name)
        # add the model to the class record
        cls.model = self.model


class PeeweeObjectTypeMeta(type(ObjectType)):

    options_class = PeeweeObjectTypeOptions

    def construct(self, *args, **kwds):
        # pass the model to the class record
        self.model = self._meta.model
        # return the full class record
        return super().construct(*args, **kwds)


    def __new__(cls, name, bases, attributes, **kwds):

        full_attr = {}

        try:
            # for each field in the table
            for field in attributes['Meta'].model.fields():
                # the name of the field in the schema
                field_name = field.name[0].lower() + field.name[1:]
                # add an entry for the field we were passed
                full_attr[field_name] = convert_peewee_field(field)
        # if there is no meta type defined
        except KeyError:
            # keep going
            pass
        # if there is no model defined
        except AttributeError:
            # yell loudly
            raise ValueError("PeeweeObjectsTypes must have a model.")


        # merge the given attributes ontop of the dynamic ones
        full_attr.update(attributes)

        # create the nex class records
        return super().__new__(cls, name, bases, full_attr, **kwds)



class PeeweeObjectType(ObjectType, metaclass=PeeweeObjectTypeMeta):
    """
        This class provides support for generating graphql ObjectTypes
        based on peewee models
    """
