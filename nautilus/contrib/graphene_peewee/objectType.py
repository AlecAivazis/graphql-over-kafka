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
        # if there is a Meta class defined
        if 'Meta' in attributes:
            try:
                # if the meta class designates a model
                model = attributes['Meta'].model
            # if there is no model defined
            except AttributeError:
                # yell loudly
                raise ValueError("PeeweeObjectsTypes must have a model.")

            # for each field in the table
            for field in model.fields():
                # add an entry for the field we were passed
                full_attr[field.name] = convert_peewee_field(field)

        # merge the given attributes ontop of the dynamic ones
        full_attr.update(attributes)

        # create the nex class records
        return super().__new__(cls, name, bases, full_attr, **kwds)



class PeeweeObjectType(ObjectType, metaclass=PeeweeObjectTypeMeta):
    """
        This class provides support for generating graphql ObjectTypes
        based on peewee models
    """
