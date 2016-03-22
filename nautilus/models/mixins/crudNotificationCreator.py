# external imports
from playhouse.signals import post_save, post_delete
# local imports
from nautilus.network.amqp import dispatch_action
from nautilus.conventions.actions import get_crud_action

# peewee support for signals from from a playhouse extension:
# http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#signals

class CRUDNotificationCreator:
    """
        This mixin class provides basic crus event publishing when the model
        is mutated, following nautilus conventions.
    """


    nautilus_base = True # required to prevent self-application on creation


    @classmethod
    def dispatch_alert(cls, action_type, target):
        dispatch_action(
            action_type=get_crud_action(action_type, cls.__name__, status="success"),
            payload=target.__json__(),
        )


    @classmethod
    def on_creation(cls):
        try:
            # perform super behavior before we do anything else
            super().on_creation()
        # if on_creation does not exist
        except AttributeError:
            # we are not extending a nautilus model - yell loudly
            raise ValueError('CRUDNotificationCreator must mix into a ' + \
                                                                ' base model')

        # TODO: failure events????

        @post_save(sender=cls)
        def post_save_handler(model_class, instance, created):
            # if the model was created for the first time
            if created:
                cls.dispatch_alert('create', instance)
            # otherwise the model was updated
            else:
                cls.dispatch_alert('update', instance)

        @post_delete(sender=cls)
        def post_delete_handler(model_class, instance):
            # let everyone know
            cls.dispatch_alert('delete', instance)
