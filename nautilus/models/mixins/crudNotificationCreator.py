# external imports
from sqlalchemy import event
# local imports
from nautilus.network import dispatchAction

class CRUDNotificationCreator:

    nautilus_base = True # required to prevent self-application on creation

    @classmethod
    def addListener(cls, db_event, action_type):
        # on event, dispatch the appropriate action
        @event.listens_for(cls, db_event)
        def dispatchCRUDAction(mapper, connection, target):
            """ notifies the network of the new user model """
            dispatchAction({
                'type': '{}_{}'.format(cls.__name__.lower(), type),
                'payload': target.__json__(),
            })


    @classmethod
    def onCreation(cls):
        # perform the intended behavior
        super().onCreation()
        # add the crud action emitters
        cls.addListener('after_insert', 'create_success')
        cls.addListener('after_delete', 'delete_success')
        cls.addListener('after_update', 'update_success')
