# external imports
from graphene import List, with_context
from graphene.relay import ConnectionField
# local imports
from nautilus.api.objectTypes import ServiceObjectType
from nautilus.api.objectTypes.serviceObjectType import serivce_objects
from nautilus.api.filter import args_for_model


class BaseConnection(List):
    """
        A field that encapsultes a connection with another GraphQL object.

        Args:

            target (str or ObjectType): The target object type. If target is a
                SerivceObjectType then the remote data lookup is automated using the
                target object's meta service attribute.

            relationship (str: "one" or "many"): The kind of relationship that this
                connection encapsultes. If set to "many" the connection will result in
                a list whereas if it is set to "one" the connection will result in the
                object type itself.


        Example:

            For an example, see the getting started guide.

    """

    def __init__(self, target, relationship='many', **kwds):

        # perform auto resolve when:
            # a resolver wasn't explicity specified
            # we are targetting a service object either explicitly or via a str
        perform_resolve = 'resolver' not in kwds and \
                            (isinstance(target, str) or \
                                issubclass(target, ServiceObjectType))

        # the field to use as the list
        list_wrapper = List(target)

        # if the target is a service service model
        if hasattr(target, 'service') and hasattr(target.service, 'model'):
            # add the model's args to the field
            kwds['args'] = args_for_model(target.service.model)


        # if we're not supposed to perform the resolve
        if not perform_resolve:
            # just instantiate a field with the wrapper
            super().__init__(type=list_wrapper, **kwds)
            # and don't do anything else
            return

        # we are supposed to perform the resolve

        # if the relationship is a value we dont yet support
        if relationship != 'many':
            # yell loudly
            raise ValueError('single relationships are not yet supported')

        # save references to constructor arguments
        self.target = target
        self.relationship = relationship

        # set the resolver if a service was specified
        kwds['resolver'] = self._resolve

        super().__init__(of_type=target, **kwds)


    def resolve_service(self, args, context, info):
        """
            This function performs the actual resolution of the service.
            Not implemented in this class - left up to subclasses.
        """
        raise NotImplementedError


    # Internal / Utility functions

    @with_context
    def _resolve(self, args, context, info):
        # make a normal dictionary out of the immutable one we were given
        args = query_args if isinstance(query_args, dict) \
                                else query_args.to_data_dict()

        # if we were given a string to target
        if isinstance(self.target, str):
            # if the string points to a service object we recognize
            if self.target in serivce_objects:
                # grab the service object with the matching name
                self.target = serivce_objects[self.target]
            # otherwise the string target does not designate a service object
            else:
                # yell loudly
                raise ValueError("Please provide a string designating a " + \
                                    "ServiceObjectType as the target for " + \
                                    "a connection.")

        # call the public facing function
        return self.resolve_service(instance, args, context, info)


    def _service_name(self, target):
        try:
            # return the name of the target
            return target.service.name
        # if it does not have the name attribute
        except AttributeError as err:
            # if the target is a string
            if isinstance(target, str):
                return target
            # otherwise the service is unknown
            raise err
